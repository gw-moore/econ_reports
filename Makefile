RUN_DATE=$(shell date +%F)

report: papermill html

papermill:
	papermill notebooks/$(report).ipynb \
	site/source/notebooks/$(report)_$(RUN_DATE).ipynb

html:
	jupyter nbconvert site/source/notebooks/$(report)_$(RUN_DATE).ipynb \
	--to html --output-dir site/source/html/ \
	--TagRemovePreprocessor.enabled=True \
	--TagRemovePreprocessor.remove_input_tags="remove_input" \
	--TagRemovePreprocessor.remove_cell_tags="remove_cell"

html_from_source:
	jupyter nbconvert dev_notebooks/$(notebook) \
	--to html --output-dir dev_notebooks/test_html/ \
	--TagRemovePreprocessor.enabled=True \
	--TagRemovePreprocessor.remove_input_tags="remove_input" \
	--TagRemovePreprocessor.remove_cell_tags="remove_cell"
