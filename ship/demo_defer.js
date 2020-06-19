// Provided by Mozilla

var pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

var pdfDoc = null,
	pageNum = 1,
	pageRendering = false,
	pageNumPending = null,
	scale = 0.8,
	canvas = document.getElementById('the-canvas'),
	ctx = canvas.getContext('2d');

function renderPage(num) {
	pageRendering = true;
	pdfDoc.getPage(num).then(function (page) {
		var viewport = page.getViewport({
			scale: scale
		});
		canvas.height = viewport.height;
		canvas.width = viewport.width;
		var renderContext = {
			canvasContext: ctx,
			viewport: viewport
		};
		var renderTask = page.render(renderContext);
		renderTask.promise.then(function () {
			pageRendering = false;
			if (pageNumPending !== null) {
				renderPage(pageNumPending);
				pageNumPending = null;
			}
		});
	});
	document.getElementById('page_num').textContent = num;
}

function queueRenderPage(num) {
	if (pageRendering) {
		pageNumPending = num;
	} else {
		renderPage(num);
	}
}

function onPrevPage() {
	if (pageNum <= 1) {
		return;
	}
	pageNum--;
	queueRenderPage(pageNum);
}
document.getElementById('prev').addEventListener('click', onPrevPage);

function onNextPage() {
	if (pageNum >= pdfDoc.numPages) {
		return;
	}
	pageNum++;
	queueRenderPage(pageNum);
}
document.getElementById('next').addEventListener('click', onNextPage);

pdfjsLib.getDocument(url).promise.then(function (pdfDoc_) {
	pdfDoc = pdfDoc_;
	document.getElementById('page_count').textContent = pdfDoc.numPages;
	renderPage(pageNum);
});