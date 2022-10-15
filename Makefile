RUN_DATE=$(shell date +%F)

report: papermill html

papermill:
	papermill econ_reports/$(report).ipynb \
	output/papermill_reports/$(report)_$(RUN_DATE).ipynb

html:
	jupyter nbconvert output/papermill_reports/$(report).ipynb \
	--to html --output ../output/html/$(report)_$(RUN_DATE).html \
	--TagRemovePreprocessor.enabled=True \
	--TagRemovePreprocessor.remove_input_tags="remove_input" \
	--TagRemovePreprocessor.remove_cell_tags="remove_cell"

html_from_source:
	jupyter nbconvert econ_reports/$(report).ipynb \
	--to html --output ../output/html/$(report)_$(RUN_DATE).html \
	--TagRemovePreprocessor.enabled=True \
	--TagRemovePreprocessor.remove_input_tags="remove_input" \
	--TagRemovePreprocessor.remove_cell_tags="remove_cell"
