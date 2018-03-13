def header():
    header = """
    <!DOCTYPE html>
        <html lang="en-US" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="robots" content="noindex">
        <meta name="googlebot" content="noindex">
        <meta name="author" content="Eric Laslo">
        <meta name="description" content="IS1061 ERL67">
        <link rel="stylesheet" type="text/css" href="./static/style.css">
        <link rel="icon" type="image/x-icon" href="http://ericlaslo.com/assets/icons/faviconf0.ico">
        <script src="http://ericlaslo.com/assets/code/footerbar.js" type="text/javascript"></script>
        <script src="http://ericlaslo.com/assets/code/color.js" type="text/javascript"></script>
        <title>Flask</title>
        </head>
        <body id="page">
        """
    return header

def footer():
    footer = """
        <script type='text/javascript'>
            colorize(['page']);
            colorizeText(['page'], false);
            footerBar();
        </script>
        </body>
        </html>
        """
    return footer

def setTitle(pageTitle):
    title = "<script>document.title = \'" 
    title += pageTitle
    title += "\';</script>"
    return title