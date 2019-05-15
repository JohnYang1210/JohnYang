from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
from quitter import Quitter 
import sys
def Press():
	getname=askopenfilenames(title='打开',
		filetypes=[('dwg','.dwg'),
		('xlsx','.xlsx'),
		('txt','.txt'),
		('pdf','.pdf'),
		('doc','.doc'),
		('docx','.docx'),
		('all','*.*')])
	return getname		
def DoIt(change_group):
	for i in range(len(change_group)):
		if os.path.exists(change_group[i][1]):
			showerror('Warnning','被修改文件夹已存在')
			sys.exit()
		else:
			try:
				os.renames(change_group[i][0],change_group[i][1])
			except:
				showerror('Error','Error')
				sys.exit()
	showinfo('Done','已全部修改完毕')


class ExtractFileName(Frame):
	def __init__(self,parent=None,**options):
		Frame.__init__(self,parent,**options)
		self.pack()
		self.names=()
		
		Button(self,text='抽取文件名',command=self.ExtratPress,width=15).pack(side=TOP)
		Button(self,text='保存至',command=self.SaveAs,width=15).pack(side=BOTTOM)
	def ExtratPress(self):
		self.names=Press()
	def SaveAs(self):
		NameFile=asksaveasfile(filetypes=[('txt','.txt')])
		for name in self.names:
			extention=os.path.splitext(name)[1]                                   #allow extracting names file with different extensions 
			written_name=os.path.split(name)[1].split(extention)[:-1][0]
			NameFile.write(written_name+'\n')
		NameFile.close()

class ChangeFileName(Frame):
	def __init__(self,parent=None,**options):
		Frame.__init__(self,parent,**options)
		self.pack()
		self.filenamefile=''
		self.path=''
		self.extension=''
		self.changing_files=''
		self.changed_files=''
		self.change_group=''

		Button(self,text='读入文件名文件',command=self.InputFileNameFile,width=15).pack()
		Button(self,text='选择修改文件',command=self.Select,width=15).pack()
		Button(self,text='批量修改',command=self.Change,width=15).pack()
	def InputFileNameFile(self):
		"""
		get the filenamefile's file
		"""
		self.filenamefile=askopenfilename(filetypes=[("txt","txt")])
	def Select(self):
		"""
		get the being-replaced file names
		"""
		self.changed_files=list(Press())

	def Change(self):
		ChangedFiles=self.changed_files
		try:
			self.path=os.path.split(ChangedFiles[0])[0]
			self.extension=os.path.splitext(ChangedFiles[0])[1]
		except IndexError:
			showwarning('NO FILE','请先选择修改文件')
			sys.exit()
		ChangingFiles=[]
		try:
			for chgname in open(self.filenamefile):
				ChangingFiles.append(os.path.join(self.path,chgname.strip()+self.extension))
		except FileNotFoundError :
			showwarning('NO FILE','请先读入文件名文件')
			sys.exit()
		self.changing_files=ChangingFiles
		if len(self.changing_files)!=len(self.changed_files):
				showerror('Error','待修改文件数量与文件修改名数量不同！')
				sys.exit()
		else:
			self.change_group=list(zip(self.changed_files,self.changing_files))
			self.Show()
		# print(self.changing_files,self.changed_files)
	def Show(self):
		win=Toplevel()
		win.title('信息校对')
		Label(win,text='对应关系表',fg='red').pack()
		frm1=Frame(win)
		frm2=Frame(win)
		frm1.pack(side=LEFT)
		frm2.pack(side=RIGHT)
		Label(frm1,text='待替换文件名',fg='red').pack()
		for i in range(len(self.changed_files)):
			Label(frm1,text=self.changed_files[i]).pack()
		Label(frm2,text='替换文件名称',fg='red').pack()
		for i in range(len(self.changing_files)):
			Label(frm2,text=self.changing_files[i]).pack()
		Button(win,text='确定',command=lambda:DoIt(self.change_group)).pack(side=BOTTOM)
		win.focus_set()
		win.grab_set()
		win.wait_window()

if __name__=='__main__':
	root=Tk()
	root.title('BatchReName')
	root.iconbitmap('BatchReName.ico')
	frame1=Frame(root)
	frame1.pack(side=TOP)
	frame2=Frame(root)
	frame2.pack(side=TOP)
	frame3=Frame(root)
	frame3.pack(side=BOTTOM)	
	Label(frame1,text='批量获取文件名',fg='red').pack(side=LEFT)
	Label(frame1,text='批量修改文件名',fg='red').pack(side=RIGHT)
	ExtractFileName(frame2).pack(side=LEFT)
	ChangeFileName(frame2).pack(side=RIGHT)
	Quitter(frame3).grid(row=0,column=0)
	Label(frame3,text='Made by JohnYang',font=('times',10,'roman'),fg='blue').grid(row=0,column=1)
	root.mainloop()
	

















