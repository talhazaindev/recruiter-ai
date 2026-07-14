import opendataloader_pdf

# Batch all files in one call — each convert() spawns a JVM process, so repeated calls are slow
opendataloader_pdf.convert(
    input_path=["cvs/cvs/cv7.pdf"],
    #input_path=["cvs_test/cv3.pdf"],
    output_dir="temp",
    format="json"
)