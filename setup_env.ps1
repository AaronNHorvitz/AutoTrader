# setup_env.ps1
$envName = "autotrader"

# Check if mamba is installed
if (-not (Get-Command mamba -ErrorAction SilentlyContinue)) {
    Write-Host "Mamba not found. Installing mamba in the base environment..."
    conda install mamba -c conda-forge -y
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install mamba. Falling back to conda..."
    }
}

# Check if the environment exists
if (conda env list | Select-String "^$envName\s") {
    Write-Host "Environment '$envName' already exists. Removing it..."
    conda env remove -n $envName
}

Write-Host "Creating environment '$envName' from environment.yaml..."
# Use mamba if available, fall back to conda if not
if (Get-Command mamba -ErrorAction SilentlyContinue) {
    mamba env create -f environment.yaml
} else {
    conda env create -f environment.yaml
}

Write-Host "Environment setup complete. Activate with: conda activate $envName"