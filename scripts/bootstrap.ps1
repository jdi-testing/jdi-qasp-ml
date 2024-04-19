param(
    [Parameter(HelpMessage="Branch used as a source for downloading files")]
    [string]$Branch = 'master',
    [Parameter(HelpMessage="Amount of allowed parallel Selenium sessions")]
    [int]$CoresToUse = (Get-WmiObject -Class Win32_Processor).NumberOfLogicalProcessors,
    [Parameter(HelpMessage="Docker image label to pull")]
    [string]$Label = 'latest',
    [Parameter(HelpMessage="Docker Compose pull policy")]
    [string]$PullPolicy = 'always',
    [Parameter(HelpMessage="Run Docker Compose in 'detached' mode")]
    [switch]$Detached,
    [Parameter(HelpMessage="Do not remove old Docker resources with the same label")]
    [switch]$NoCleanup
)

function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath
    )
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($Url, $OutputPath)
}

# Remove old Docker resources if cleanup flag is not set
if (-not $NoCleanup) {
    $labelSelector = "org.jdi-qasp-ml.version_label=$Label"
    docker stop $(docker ps -qf "label=$labelSelector") 2>$null
    docker container rm -f $(docker ps -qaf "label=$labelSelector") 2>$null
    docker volume rm -f $(docker volume ls -qf "label=$labelSelector") 2>$null
    docker network rm -f $(docker network ls -qf "label=$labelSelector") 2>$null
    Remove-Item -Path "docker-compose.yaml", "docker-compose.override.yaml", "browsers.json", ".env" -ErrorAction SilentlyContinue
    Remove-Item -Recurse "analyzed_page" -ErrorAction SilentlyContinue
}

$RepoUrl = "https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/$Branch"

Download-File -Url ("$RepoUrl/docker-compose.yaml") -OutputPath "docker-compose.yaml"
Download-File -Url ("$RepoUrl/browsers.json.template") -OutputPath "browsers.json"
New-Item -ItemType Directory -Name "analyzed_pages"

(Get-Content "browsers.json") -replace "CURRENT_DIR", ((Get-Location).Path -replace "\\", "/") | Set-Content "browsers.json"

$randomNumber = Get-Random -Minimum 0 -Maximum 99999999
$hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($randomNumber.ToString()))
$randomString = ([System.BitConverter]::ToString($hash) -replace '-', '').Substring(0, 8)
$NetworkName = ("jdi-qasp-ml-$randomString")

@"
JDI_VERSION_LABEL=$Label
SELENOID_PARALLEL_SESSIONS_COUNT=$CoresToUse
JDI_DEFAULT_NETWORK_NAME=$NetworkName
"@ | Set-Content -Path ".env"

if ($Label -ne 'latest') {
    Download-File -Url ("$RepoUrl/docker-compose.override.arbitrary-tag.yaml") -OutputPath "docker-compose.override.yaml"
}

# Start Docker Compose
if ($Detached) {
    docker compose up -d --pull $PullPolicy
} else {
    docker compose up --pull $PullPolicy
}
