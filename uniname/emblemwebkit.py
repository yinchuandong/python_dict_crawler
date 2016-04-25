# import sys  
# from PyQt4.QtGui import *  
# from PyQt4.QtCore import *  
# from PyQt4.QtWebKit import *  
# from lxml import html 

# class Render(QWebPage):  
#   def __init__(self, url):  
#     self.app = QApplication(sys.argv)  
#     QWebPage.__init__(self)  
#     self.loadFinished.connect(self._loadFinished)  
#     self.mainFrame().load(QUrl(url))  
#     self.app.exec_()  
  
#   def _loadFinished(self, result):  
#     self.frame = self.mainFrame()  
#     self.app.quit()

# # url = 'http://pycoders.com/archive/'  
# url = 'https://www.google.com.au/#newwindow=1&q=USI+Universita+della+Svizzera+italiana++USI+University+of+Lugano'
# #This does the magic.Loads everything
# r = Render(url)  
# #result is a QString.
# result = r.frame.toHtml()
# #QString should be converted to string before processed by lxml
# formatted_result = str(result.toAscii())
# # print formatted_result
# with open('google_test_2.html', 'w') as f:
#     f.write(formatted_result)


from ghost import Ghost

if __name__ == "__main__":
    # url = 'https://www.google.com.au/#newwindow=1&q=USI+Universita+della+Svizzera+italiana++USI+University+of+Lugano'
    url = 'https://www.google.com.au/?q=University+of+Lugano&newwindow=1'
    ghost = Ghost()
    with ghost.start() as session:
        page, extra_resources = session.open(url)
        print page.http_status
        print page.content
        with open('google_test_2.html', 'w') as f:
            f.write(page.content)






