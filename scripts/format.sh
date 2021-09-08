WORKDIR=$(pwd)

echo "Formatting..."
cd "$WORKDIR/server" && isort . && black .
