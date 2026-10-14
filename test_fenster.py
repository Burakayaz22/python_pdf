import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QFileDialog, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QAction, QImage, QPixmap
import pymupdf
from pdf_tools.pdf_merge import pdfmerge


class PdfViewer(QMainWindow):
    def __init__(self):              # der Konstruktor
        super().__init__()
        self.setWindowTitle("B PDF-Editor")
        self.resize(900,1000)
        self.pfad =None
        self.dokument = None

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        oeffnen = QAction("Öffnen", self)
        toolbar.addAction(oeffnen)
        oeffnen.triggered.connect(self.datei_oeffnen)

        save = QAction("Save",self)
        toolbar.addAction(save)
        save.triggered.connect(self.datei_save)

        menue= self.menuBar().addMenu("Edit")
        merge=QAction("Merge",self)
        delet=QAction("Remove",self)
        split=QAction("Split",self)

        menue.addAction(merge)
        merge.triggered.connect(self.datei_mergen)
        menue.addAction(delet)
        menue.addAction(split)

        

    def datei_oeffnen(self):
        pfad, _ = QFileDialog.getOpenFileName(self, "Open PDF-File", "", "PDF (*.pdf)")
        if not pfad: # Abbrechen -> leerer Text -> nichts tun
            return
        self.pfad=pfad
        self.dokument = pymupdf.open(self.pfad)
        print("Seitenanzahl:", len(self.dokument))
        print("Dateipfad:", self.dokument.name)

        self.pdf_open()        
        
    def seite_oeffnen(self, page):
        seite = self.dokument[page]
        pix = seite.get_pixmap(dpi=100)
        bild = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        
        label = QLabel()
        label.setPixmap(QPixmap.fromImage(bild))
        return label

    def pdf_rendern(self):
        pages=0
        total_page_count=len(self.dokument)
        layout = QVBoxLayout()
        while(pages<total_page_count):
            label=self.seite_oeffnen(pages)
            layout.addWidget(label)
            pages += 1

        return layout

    def pdf_open(self):
        behaelter = QWidget()
        behaelter.setLayout(self.pdf_rendern())

        scroll = QScrollArea()
        scroll.setWidget(behaelter)
        self.setCentralWidget(scroll) 

    def datei_mergen(self):
        if not self.dokument:
            return
        pfad, _ = QFileDialog.getOpenFileName(self,"Open PDF-File", "", "PDF (*.pdf)")
        if not pfad: # Abbrechen -> leerer Text -> nichts tun
            return 
        
        pdf = pdfmerge(pfad, self.dokument)
        self.dokument=pdf
        self.pdf_open()

    def datei_save(self):
        if not self.dokument:
            return
        pfad, _ = QFileDialog.getSaveFileName(self,"Save PDF-File", "", "PDF (*.pdf)")
        if pfad==self.pfad:
            temp_pfad = pfad + ".temp"
            self.dokument.save(temp_pfad)
            self.dokument.close()
            os.replace(temp_pfad,pfad)
            self.dokument = pymupdf.open(self.pfad)
        else:    
            self.dokument.save(pfad)





        
            



app = QApplication(sys.argv)
fenster = PdfViewer()
fenster.show()
sys.exit(app.exec())






