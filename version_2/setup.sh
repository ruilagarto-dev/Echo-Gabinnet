#!/bin/bash

VENV_NAME="myvenv"
PYTHON="$VENV_NAME/bin/python"
PIP="$VENV_NAME/bin/pip"

install() {
    if [ ! -d "$VENV_NAME" ]; then
        python3 -m venv "$VENV_NAME"
    fi

    "$PIP" install --upgrade pip

    echo -e "\n📦 \033[1;33mInstalando pacotes do requirements.txt...\033[0m"
    "$PIP" install -r requirements.txt

    echo -e "\n✅ \033[1;32mInstalação concluída!\033[0m"
}

clean() {
    echo -e "\n🧹 Limpando arquivos temporários, caches e dependências..."
    if [ -d "$VENV_NAME" ]; then
        "$PIP" freeze | xargs -r "$PIP" uninstall -y
        rm -rf "$VENV_NAME"
    fi
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.py[co]" -delete
    rm -rf .pytest_cache .mypy_cache .coverage dist build

    echo -e "\033[1;31m❌ TODAS as dependências e caches removidos.\033[0m"
}

sync() {
    echo -e "\n🔄 Sincronizando dependências..."
    "$PIP" freeze > requirements.txt
    echo -e "\033[1;32m✅ requirements.txt atualizado!\033[0m"
}

run() {
    echo -e "\n🚀 Iniciando aplicação..."
    sleep 0.5
    "$PYTHON" src/main.py
}

# Menu
case "$1" in
    install) install ;;
    clean) clean ;;
    sync) sync ;;
    run) run ;;
    *) 
        echo -e "\nUso: ./setup.sh [install|clean|sync|run]"
        ;;
esac
