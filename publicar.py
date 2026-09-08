#!/usr/bin/env python3
"""
Publica o site sergiocardoso.pro.br.

MODELO: a pasta site/ É o site. O que está nela vai ao ar; o que não está, não vai.
Você arruma a pasta com a mão e depois publica.

TRÊS COMANDOS:

    python3 publicar.py sincronizar   traz de fora as cópias que envelhecem
                                      (dados e atividades). Não publica.
    python3 publicar.py conferir      mostra o que iria ao ar. Não publica.
    python3 publicar.py               publica o que está na pasta.

DUAS REGRAS:

  1. Nome começando com "_" nunca é publicado, seja arquivo ou pasta, em qualquer
     profundidade. Use _oculto/, _rascunho/, _arquivo/ para tirar do ar sem
     apagar. Esses nomes também estão no .gitignore, então não vão nem para o
     GitHub.
  2. Arquivo com nome suspeito (gabarito, prova, presença, notas) FAZ A
     PUBLICAÇÃO PARAR, com a lista na tela. Renomeie ou mova para uma pasta "_".

ÍNDICE AUTOMÁTICO: uma pasta ganha index.html gerado só se tiver dentro dela um
arquivo vazio chamado _gerar_indice. Sem esse arquivo, a página é sua e o script
nunca toca nela.
"""
import html, re, shutil, subprocess, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
UFC = Path.home() / "Documents/UFC/disciplinas"
REPO = "sergioce20/sergioce20.github.io"
RAMO = "main"

FC = UFC / "financas_corporativas/2026-2"
DESTINO_FC = "ufc/financas-corporativas/2026-2"

# O QUE VEM DE FORA. Só entra aqui o que envelhece e cuja cópia velha causa dano.
# Slides e textos NÃO entram: ficam no SIGAA, para não existirem em duas versões.
SINCRONIZAR = [
    {"de": FC / "dados", "para": f"{DESTINO_FC}/dados", "glob": "**/*",
     "descricao": "pacote de dados congelado"},
    {"de": FC / "aulas", "para": f"{DESTINO_FC}/atividades", "glob": "*/**/*_ALUNO.ipynb",
     "plano": True, "descricao": "notebooks das tarefas"},
    {"de": FC / "aulas", "para": f"{DESTINO_FC}/atividades", "glob": "*/**/*_ALUNO.xlsx",
     "plano": True, "descricao": "planilhas das tarefas"},
]

BLOQUEIO = re.compile(r"(?i)(gabarito|prova|presenc|notas?_|conceito|matricula)")
IGNORAR_SEMPRE = {".git", ".DS_Store", "__pycache__", "publicar.py", "LEIA-ME.md", "Publicar site.command"}


def oculto(caminho: Path) -> bool:
    """True se qualquer parte do caminho começa com _ ou está na lista fixa."""
    rel = caminho.relative_to(SITE)
    return any(p.startswith("_") or p in IGNORAR_SEMPRE for p in rel.parts)


def arquivos_publicaveis():
    for f in sorted(SITE.rglob("*")):
        if f.is_file() and not oculto(f):
            yield f


def tamanho(p):
    n = p.stat().st_size
    for u in ("B", "KB", "MB"):
        if n < 1024 or u == "MB":
            return f"{n:.1f} {u}".replace(".0 ", " ")
        n /= 1024


def sincronizar():
    print("Trazendo de fora as cópias que envelhecem.\n")
    for regra in SINCRONIZAR:
        origem, destino = regra["de"], SITE / regra["para"]
        if not origem.exists():
            print(f"  ! origem não encontrada: {origem}")
            continue
        destino.mkdir(parents=True, exist_ok=True)
        novos = atualizados = 0
        for f in sorted(origem.glob(regra["glob"])):
            if not f.is_file() or f.name.startswith(".") or "arquivos_antigos" in f.parts:
                continue
            alvo = destino / f.name if regra.get("plano") else destino / f.relative_to(origem)
            alvo.parent.mkdir(parents=True, exist_ok=True)
            if not alvo.exists():
                novos += 1
            elif f.stat().st_mtime > alvo.stat().st_mtime or f.stat().st_size != alvo.stat().st_size:
                atualizados += 1
            else:
                continue
            shutil.copy2(f, alvo)
        print(f"  {regra['descricao']}: {novos} novo(s), {atualizados} atualizado(s)"
              f"  ->  {regra['para']}/")
    print("\nAgora ajuste a pasta site/ como quiser e rode:  python3 publicar.py")


def conferir(silencioso=False):
    """Devolve a lista de bloqueios. Se não for silencioso, imprime o inventário."""
    bloqueados = [f for f in arquivos_publicaveis() if BLOQUEIO.search(f.name)]
    if not silencioso:
        por_pasta = {}
        for f in arquivos_publicaveis():
            por_pasta.setdefault(f.parent.relative_to(SITE).as_posix() or ".", []).append(f)
        print("O QUE ESTÁ NO AR (ou iria, se você publicar agora):\n")
        for pasta in sorted(por_pasta):
            print(f"  {pasta}/")
            for f in por_pasta[pasta]:
                print(f"      {f.name}  ({tamanho(f)})")
        ocultos = [p for p in SITE.rglob("_*") if p.name.startswith("_")]
        if ocultos:
            print("\nFORA DO AR (começa com _, nem vai para o GitHub):")
            for p in sorted(ocultos):
                print(f"  {p.relative_to(SITE)}")
    if bloqueados:
        print("\n*** BLOQUEADO. Estes nomes não podem ser publicados: ***")
        for f in bloqueados:
            print(f"  {f.relative_to(SITE)}")
        print("Renomeie ou mova para uma pasta começando com _.")
    return bloqueados


def gerar_indices():
    """Gera index.html só nas pastas que têm o marcador _gerar_indice."""
    feitos = []
    for marcador in SITE.rglob("_gerar_indice"):
        pasta = marcador.parent
        arqs = [f for f in sorted(pasta.rglob("*"))
                if f.is_file() and not oculto(f) and f.name != "index.html"]
        if not arqs:
            continue
        grupos = {}
        for f in arqs:
            grupos.setdefault(f.parent.relative_to(pasta).as_posix() or ".", []).append(f)
        base = "/" + pasta.relative_to(SITE).as_posix()
        secoes = []
        for sub in sorted(grupos):
            titulo = "arquivos" if sub == "." else sub
            pre = "" if sub == "." else sub + "/"
            tr = "".join(
                f'<tr><td><a href="{base}/{pre}{html.escape(f.name)}">'
                f'{html.escape(f.name)}</a></td><td>{tamanho(f)}</td></tr>' for f in grupos[sub])
            secoes.append(f"<h2>{html.escape(titulo)}</h2>"
                          f"<table><tr><th>arquivo</th><th>tamanho</th></tr>{tr}</table>")
        titulo_pagina = (pasta / "_titulo.txt").read_text(encoding="utf-8").strip() \
            if (pasta / "_titulo.txt").exists() else pasta.name
        (pasta / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo_pagina)} · Sérgio Cardoso</title>
<link rel="stylesheet" href="/assets/estilo.css">
</head>
<body>
<header class="capa">
  <div class="limite">
    <a class="volta" href="/">Sérgio Cardoso</a>
    <h1>{html.escape(titulo_pagina)}</h1>
  </div>
</header>
<main class="limite">{"".join(secoes)}</main>
<footer class="limite"><p>Material didático sob licença
<a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br">CC BY 4.0</a>,
salvo indicação em contrário no próprio arquivo.</p></footer>
</body>
</html>
""", encoding="utf-8")
        feitos.append(pasta.relative_to(SITE).as_posix())
    return feitos


def carimbar_css():
    """Poe a versao da folha de estilo no link de todas as paginas, para que
    ninguem continue vendo o desenho antigo por cache do navegador."""
    import hashlib
    css = SITE / "assets/estilo.css"
    if not css.exists():
        return
    v = hashlib.sha1(css.read_bytes()).hexdigest()[:8]
    alvo = f'href="/assets/estilo.css?v={v}"'
    n = 0
    for pag in SITE.rglob("*.html"):
        if oculto(pag):
            continue
        texto = pag.read_text(encoding="utf-8")
        novo = re.sub(r'href="/assets/estilo\.css(\?v=[0-9a-f]+)?"', alvo, texto)
        if novo != texto:
            pag.write_text(novo, encoding="utf-8")
            n += 1
    if n:
        print(f"  folha de estilo carimbada como v={v} em {n} página(s)")


def publicar():
    if conferir(silencioso=True):
        conferir()
        sys.exit(1)
    feitos = gerar_indices()
    carimbar_css()
    for f in feitos:
        print(f"  índice gerado: {f}/index.html")
    subprocess.run(["git", "fetch", "-q", "origin"], cwd=SITE, check=False)
    subprocess.run(["git", "pull", "--rebase", "-q", "origin", RAMO], cwd=SITE, check=False)
    subprocess.run(["git", "add", "-A"], cwd=SITE, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=SITE).returncode == 0:
        print("  nada mudou, nada a enviar")
        return
    subprocess.run(["git", "commit", "-m", "atualiza publicação"], cwd=SITE, check=True)
    subprocess.run(["git", "push", "-q"], cwd=SITE, check=True)
    n = sum(1 for _ in arquivos_publicaveis())
    print(f"  enviado: {n} arquivos no ar. O site atualiza em cerca de um minuto.")


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "publicar"
    if comando == "sincronizar":
        sincronizar()
    elif comando == "conferir":
        conferir()
    else:
        publicar()
