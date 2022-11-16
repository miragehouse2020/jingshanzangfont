// Main Code [Execution of script begins here]

// Collectable files
var COLLECTABLE_EXTENSIONS = ["bmp", "gif", "giff", "jpeg", "jpg", "pct", "pic", "psd", "png", "tif", "tiff"];
var destFolder, sourceFolder;

// Select the source folder
sourceFolder = new Folder("d:/git/jingshanzangfont/vcrop/")
//sourceFolder = Folder.selectDialog('Select the SOURCE folder...', '~');
//sourceFolder = new Folder("C:/Users/<Username>/Desktop/1");

if (sourceFolder != null) {
    // Select the destination folder
	destFolder = new Folder("d:/git/jingshanzangfont/vsvg/")
    //destFolder = Folder.selectDialog('Select the DESTINATION folder...', '~');
    //destFolder = new Folder("C:/Users/<Username>/Desktop/2");
}

if (sourceFolder != null && destFolder != null) {
    //getting the list of the files from the input folder
    var fileList = sourceFolder.getFiles();
    var errorList;
    var tracingPresets = app.tracingPresetsList;

    /*var TraceList = [{
            TracePreset: "ImgDraw_黑白",
            SaveName: "black"
        }, {
            TracePreset: "ImgDraw_灰度",
            SaveName: "gray"
        }, {
            TracePreset: "ImgDraw",
            SaveName: "color"
        }
    ];*/

    // 新建一个文档
    var doc = app.documents.add();
    for (var i = 0; i < fileList.length; ++i) {
        if (fileList[i]instanceof File) {
            try {
                var fileExt = String(fileList[i]).split(".").pop();
                if (isTraceable(fileExt) != true)
                    continue;
                //var destFileName = fileList[i].name.substring(0, fileList[i].name.length - fileExt.length - 1) + "_";
				var destFileName = fileList[i].name.substring(0, fileList[i].name.length - fileExt.length - 1);
                var options = getExpertOption();
                // 将图片导入
                var p = doc.placedItems.add();
                p.file = new File(fileList[i]);

                //  新建一个与图片相同大小的临时文档用于保存
                var tmpdoc = app.documents.add(DocumentColorSpace.RGB, p.width, p.height);
                var p2 = tmpdoc.placedItems.add();
                p2.file = new File(fileList[i]);
                // 描摹
                var t = p2.trace();
                //for (var j = 0; j < TraceList.length; j++) {
				t.tracing.tracingOptions.loadFromPreset(tracingPresets[14]);
				app.redraw();
				//var outfile = new File(destFolder + "/" + destFileName + TraceList[j].SaveName);
				var outfile = new File(destFolder + "/" + destFileName);
				tmpdoc.exportFile(outfile, ExportType.SVG, options);
                //}

                p.remove();
                // 关闭临时文档
                tmpdoc.close(SaveOptions.DONOTSAVECHANGES);
            } catch (err) {
                errorStr = ("Error while tracing " + fileList[i].name + ".\n" + (err.number & 0xFFFF) + ", " + err.description);
                // alert(errorStr);
                errorList += fileList[i].name + " ";
            }
        }
    }
    fileList = null;
    alert("Batch process complete.");
} else {
    alert("Batch process aborted.");
}

sourceFolder = null;
destFolder = null;

function isTraceable(ext) {
    var result = false;
    for (var i = 0; i < COLLECTABLE_EXTENSIONS.length; ++i) {
        if (ext == COLLECTABLE_EXTENSIONS[i]) {
            result = true;
            break;
        }
    }
    return result;
}

/** 导出函数参数设置
 */
function getExpertOption() {
    // Create the required options object
    var options = new ExportOptionsSVG();
    // 精度2位
    options.coordinatePrecision = 2;
    // 使用UTF8编码
    options.documentEncoding = SVGDocumentEncoding.UTF8;
    //导出字体为SVG字体
    options.fontType = SVGFontType.SVGFONT;
    return options;
}
