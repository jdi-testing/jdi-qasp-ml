# generate $N_SITES sites
N_SITES=500

npm install npm lorem-ipsum

n=0; while [[ $n -lt $N_SITES ]]; do
    echo "Generate site $n"
    export BUILD_PATH=../../data/mui_dataset/build/site-${n}
    npm run generate
    n=$((n+1));
done

