import json
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi_cache.coder import Coder

class StreamingResponseCoder(Coder):
    @classmethod
    async def encode(cls, value: StreamingResponse) -> bytes:
        # Extract serializable parts of StreamingResponse
        if isinstance(value, StreamingResponse):
            headers = dict(value.headers)
            content = b""

            # Properly await the async generator
            async for chunk in value.body_iterator:
                if not isinstance(chunk, bytes):
                    chunk = chunk.encode(value.charset)
                content += chunk

            # Prepare data for serialization
            data = {
                "status_code": value.status_code,
                "headers": headers,
                "content": content.decode('utf-8'),  # Convert to string for JSON serialization
            }
            return json.dumps(data).encode("utf-8")
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    @classmethod
    async def decode(cls, value: bytes) -> StreamingResponse:
        # Convert the cached data back into a StreamingResponse
        data = json.loads(value.decode("utf-8"))
        content = BytesIO(data["content"].encode("utf-8"))  # Convert content back to bytes
        headers = data["headers"]
        status_code = data["status_code"]
        return StreamingResponse(content=content, headers=headers, status_code=status_code)