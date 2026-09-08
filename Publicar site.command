#!/bin/zsh
# Duplo clique para abrir. Menu de publicação do site sergiocardoso.pro.br.
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || echo /usr/bin/python3)

titulo() {
  clear
  print -P "%F{blue}────────────────────────────────────────────────────────%f"
  print -P "  %BPublicação do site%b  ·  sergiocardoso.pro.br"
  print -P "%F{blue}────────────────────────────────────────────────────────%f"
  echo
}

pausa() { echo; print -P "%F{242}Pressione Enter para voltar ao menu.%f"; read -r; }

while true; do
  titulo
  echo "  1  Sincronizar        trazer de fora dados e atividades que mudaram"
  echo "  2  Conferir           ver o que está (ou iria) no ar"
  echo "  3  Publicar           enviar o que está na pasta"
  echo "  4  Sincronizar e publicar     (o caminho mais comum)"
  echo
  echo "  5  Abrir a pasta do site no Finder"
  echo "  6  Abrir o site no navegador"
  echo
  echo "  0  Sair"
  echo
  print -n "  Opção: "
  read -r opcao
  echo

  case "$opcao" in
    1) "$PY" publicar.py sincronizar; pausa ;;
    2) "$PY" publicar.py conferir; pausa ;;
    3) "$PY" publicar.py; pausa ;;
    4) "$PY" publicar.py sincronizar && echo && "$PY" publicar.py; pausa ;;
    5) open .; ;;
    6) open "https://sergiocardoso.pro.br"; ;;
    0) echo "  Até logo."; sleep 1; exit 0 ;;
    *) print -P "  %F{red}Opção inválida.%f"; sleep 1 ;;
  esac
done
