import os
import win32com.client

pptx_path = os.path.abspath('IBM_SpaceX_Capstone/Data Science Capstone Project Report.pptx')
pdf_path = os.path.abspath('IBM_SpaceX_Capstone/Data Science Capstone Project Report.pdf')

try:
    powerpoint = win32com.client.Dispatch('PowerPoint.Application')
    # Open presentation (FileName, ReadOnly, Untitled, WithWindow)
    presentation = powerpoint.Presentations.Open(pptx_path, True, False, False)
    # 32 = ppSaveAsPDF
    presentation.SaveAs(pdf_path, 32)
    presentation.Close()
    powerpoint.Quit()
    print('Successfully converted to PDF:', pdf_path)
except Exception as e:
    print('Could not convert with PowerPoint COM:', e)
