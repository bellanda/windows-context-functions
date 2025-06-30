import pathlib
import sys
import time

import fitz


def pdf_para_pixmaps(pdf_path: pathlib.Path, dpi: int) -> list[fitz.Pixmap]:
    """
    Rasteriza cada página do PDF como um pixmap (imagem em memória).

    Args:
        pdf_path (Path): Caminho para o arquivo PDF.
        dpi      (int): Resolução (dots per inch).

    Returns:
        List[fitz.Pixmap]: Lista de pixmaps rasterizados.
    """
    doc = fitz.open(str(pdf_path))
    pixmaps: list[fitz.Pixmap] = []
    # Ajuste de escala: 72 DPI é o padrão, então calculamos fator de escala
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        pixmaps.append(pix)
    doc.close()
    return pixmaps


def pixmaps_para_pdf(pixmaps: list[fitz.Pixmap], output_pdf: pathlib.Path):
    if not pixmaps:
        raise ValueError("Nenhum pixmap para compor o PDF.")

    new_doc = fitz.open()
    for pix in pixmaps:
        # converte para RGB (remove alfa) e gera bytes JPEG
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)  # tira canal alfa
        img_bytes = pix.tobytes("jpeg", jpg_quality=75)  # qualidade entre 50–85

        # cria a página com o tamanho da imagem
        page = new_doc.new_page(width=pix.width, height=pix.height)
        # insere a imagem cobrindo toda a página
        page.insert_image(page.rect, stream=img_bytes, keep_proportion=True)

        # >>> AQUI: insere um texto simples no rodapé (por exemplo)
        text = "PDF gerado automaticamente – sem texto original"
        # posição (x, y) em pontos; ajuste conforme quiser
        pos = fitz.Point(20, pix.height - 30)
        page.insert_text(
            pos,
            text,
            fontname="helv",  # fonte Helvetica
            fontsize=8,  # tamanho pequeno
            color=(0, 0, 0),  # cor preta
        )

    # ativa deflate (zlib) e limpa objetos não usados
    new_doc.save(str(output_pdf), deflate=True, clean=True, garbage=4)
    print(f"PDF gerado em: {output_pdf}")


start_time = time.time()
SOURCE_PATH = pathlib.Path(sys.argv[1])
DESTINATION_PATH = SOURCE_PATH.parent / (SOURCE_PATH.stem + "-images")
DESTINATION_PATH.mkdir(parents=True, exist_ok=True)
pixmaps = pdf_para_pixmaps(SOURCE_PATH, dpi=150)

for i, pixmap in enumerate(pixmaps):
    pixmap.save(DESTINATION_PATH / f"Página {i + 1}.jpg")

# pixmaps_para_pdf(pixmaps, DESTINATION_PATH)

end_time = time.time()
print(f"Tempo de execução: {end_time - start_time} segundos")
