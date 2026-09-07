# Site sergiocardoso.pro.br

Pasta de publicação. **Não é aqui que se edita conteúdo.**
Os arquivos nascem e são editados nas pastas das disciplinas; esta pasta
só recebe cópias do que é público.

## Como publicar

No Terminal:

    cd ~/Documents/site && python3 publicar.py

O script copia, monta os índices, envia para o GitHub e o site atualiza
em cerca de um minuto. Para conferir antes de enviar:

    python3 publicar.py --so-montar

## A regra que protege o material fechado

Só é copiado o que tem **`_ALUNO` no nome do arquivo**, mais a pasta
`dados/` inteira. Gabarito, prova e lista de presença não têm `_ALUNO`
no nome, então não sobem. Pastas `arquivos_antigos` são ignoradas.

Se um arquivo precisa ficar público, renomeie-o com `_ALUNO` na origem.
Se algo público não pode mais aparecer, tire o `_ALUNO` e publique de novo.

## Para incluir outra disciplina

Abra `publicar.py` e acrescente uma entrada em `DISCIPLINAS`, com o slug,
o título e o caminho da pasta de origem.
