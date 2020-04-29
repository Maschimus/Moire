# Using python 3.6
from tkinter import *                                                   #Standart                        
from PIL import Image,ImageTk                                           ### Instalation needed
from tkinter.filedialog import askopenfilenames,askopenfilename         # Comes with TK inter
import datetime                                                         # Standart      
import matplotlib.pyplot as plt                                         # Standart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# For Moire
import matplotlib.pyplot as plt     # For ploting
import numpy as np                  # Array handling
import matplotlib.image as mpimg    # Load image
import imageio                      # Save image without yellow               
import cv2                          # Scale image
import os                           # Get fileformart
import matplotlib.animation as animation # Animation of Moire


######## PARENT GUI ################### PARENT GUI ################### PARENT GUI ###################

class PARENTGUI(Frame):
      ''' Parent Class for the basic layout of the two sites contianing
            - all relevat return values
            - windowsize
            - basic functions
      '''
            
      def __init__(self,values,master=None,saturation=0):
          
         
          ''' Initialize window and create Frame'''
          # Set main Frame and window
          Frame.__init__(self,master,background="white")     # this is main Frame
          self.master=master              # main window
          self.picture=PICTURE()          # Class for Fotos
          self.saturation_val=70          # Set default saturation
          self.values=values
          # define constants
          self.width=800            # Window length
          self.hight=500            # Window hight 
          #set background fixed to locate objects with place (x=x,y=y)
          self.pack(fill=BOTH,expand=1)
          self.master.geometry(str(self.width)+"x"+str(self.hight))
          self.master.resizable(0, 0)


          # add menu bar
          self.__menu()


      def open_file(self,button,i):
           ''' Function to open only png files
               Takes:
                         - Buttom event
               Returns:
                         - name of selceted Powerpoint
                         - adds powertpoint to list
            '''
           # Open file
           name = askopenfilename(parent=self.master,filetypes =(("PowerPoint", "*.png"),("All Files","*.*")),
                                  title = "Choose a file."
                                  )

           #Using try in case user types in unknown file or closes without choosing a file.
           '''
           try:
               with open(name,'r') as UseFile:
                   print(UseFile.read())
           except:
               print("No file exists")
           '''
           # Check if nothing was selectet
                 # Do not change self.png
                 # Set buttom to deflaut value
           if(name==()):
                  empt="Click to add file "
                  name=empt.ljust(30)
                  bname=name[:20]

           # If something was selected set self.png and set buttom name
           else:
                 bname=(self.relative_name(str(name)))
                 self.values.png[i]=bname
                 bname=bname.ljust(40)
                 bname=bname[:40]
           
           self.update_btn_text(button,bname)
           # check for same size
           if(not(self.__check_size)):
                  window=ERROR(self.master,3)
                  
      def __menu(self):
          ''' Function to create menu bar'''
          # creating a menu instance
          menu = Menu(self.master)
          self.master.config(menu=menu)

          # create the file object
          file = Menu(menu)
          file.add_command(label="Exit", command=self.client_exit)
          file.add_command(label="Open File", command=self.open_file)
          menu.add_cascade(label="File", menu=file)

          # create the edit object
          edit = Menu(menu)
          # redo and undo
          edit.add_command(label="Undo",command=lambda:self.__undo())
          edit.add_command(label="Redo",command=lambda:self.__redo())
          edit.add_command(label="Clear all",command=lambda:self.__clear_all())

          #added edit to our menu
          menu.add_cascade(label="Edit", menu=edit)
          # help function refering to dokumentation of projeject
          helping = Menu(menu)
          helping.add_command(label="Online help",command=lambda:self.__open_doc())

          #added "file" to our menu
          menu.add_cascade(label="Help", menu=helping)
          
      def __check_size(self):
         return False
      
      def client_exit(self):
           ''' Function to exit'''
           exit()

      def __clear_all(self):
            self.values.reset()
            self.master.destroy()   # Destroy window
            root= Tk()              # Open new window
            window=GUI1(self.values,root)
            

      def __open_doc(self):
          ''' Function to open dokumentation'''
          webbrowser.open('http://www.gidf.de/')


      def add_photo(self,name,posx=0,posy=0):
          ''' Function to add photo
              Takes:
                    - name 
                    - place
              Retrurns
                    - Photo at this location
          '''
          load =Image.open("./Image/"+name)
          photo = ImageTk.PhotoImage(load)
          label = Label(self.master,image=photo)
          label.image=photo
          label.place(x=posx,y=posy)


      def __undo(self, event=None):
           ''' Function to undo
             contains bucks
            '''
           self.master.event_generate("<<Undo>>")
           return

      def __redo(self, event=None):
           ''' Function to redo
             contains bucks
            '''
           self.master.event_generate("<<Redo>>")
           return

      def relative_name(self,name):
             ''' Function to get name withhout relative dependence'''
             cwd = str(os.getcwd())
             if cwd in name:
                  png_name=name.replace(cwd,'')
             else:
                  name=name.replace('/', '\\')
                  if cwd in name:
                        png_name=name.replace(cwd,'')
                  else:
                        raise Exception('Folder structor not known, now returning the whole path of file')

             return(png_name[1:])




######## PARENT SIDE ################### PARENT SIDE ################### PARENT SIDE ###################

class SIDESIDE(Frame):
        ''' Parent class for other windows like Error, etc.'''
        def __init__(self, original):
              """Constructor"""
              self.original_frame = original
              self.original_frame.withdraw()
              main=Tk()
              self.main=main
              self.main.config(bg="black")
              self.main.geometry("400x300")
              Frame.__init__(self,main,background="grey")  
              self.frame=Frame(main)
              self.pack(fill=BOTH,expand=1)
              self.main.resizable(0, 0)
               
        def show(self):
              self.original_frame.update()
              self.original_frame.deiconify()
              


class VALUES():
      ''' Class to store values of all teh relevant information. 
      All other classes will inherit this class ti change the values directely
      '''
            
      def __init__(self,N=5,png=[],size=[0,0],N_png=0):
          self.N=N                     # Default numbers button
          self.png=[None]*self.N       # Create Empty list for png
          self.size=size               # Size of first loaded picture
          self.N_png=N_png             # Number of loaded png

          # Fill List of Powerpoint names with given names, if list png is not empty
          if(len(png)!=0):
                for i,name in enumerate(png):
                      self.png[i]=name
                      
   

          


      def return_values(self):
            ''' Function to return all class properties'''
            # get rid of None type objects ind png and kt_names
            png=self.__png_names()
            return(
                  png,
                  self.saturation,
                  self.pattern_width
                  )

      def __png_names(self):
            ''' Function get rid of None object in png'''
            name=[]
            for i in range(0,len(self.png)):
                  if(self.png[i]!=None):
                        name.append(self.png[i])
            return name
      def reset(self):
          self.N=5                  # Default numbers button
          self.png=[None]*self.N    # Create Empty list for Powerpoints             
          self.saturation=80
          self.pattern_width=10

   
######## MASSTER GUI ################### MASTER GUI ################### MASTER GUI ###################
class MAINGUI():
      ' Class to handel different GUIs'''
      def __init__(self):
            # Initialize class for values
            root=Tk()
            values=VALUES()
            Window=GUI1(values,root)
            root.mainloop()
                      

             
######## GUI1 ################### GUI1 ################### GUI1 ###################
class GUI1(PARENTGUI):
   ''' Class for page 1'''
   def __init__(self, values,master=None,N=5):
          PARENTGUI.__init__(self,values,master)
          self.filename=[None]*self.values.N
          # Set main Frame and window
          self.__init_window()


         

   def __init_window(self):
          self.master.title("Loading files")
              
          # Add botton merge
          mergeButton=Button(self,text="Continue",bg="red",font="Calibri 40 bold",fg="white",relief="raised",command=lambda:self.__open_page2(self.values))
          mergeButton.place(x=450,y=400)
          
          # Add botton more Files
          addmoreFilesButton=Button(self,text="Add more files",bg="white",font="Calibri 20 bold",fg="red",relief="raised",command=lambda:self.__addmore_files())
          addmoreFilesButton.place(x=450,y=350)


          # Automised N buttoms with unambiguous identity due to list
          btn=[]
          for i in range(0,self.values.N):
                 dist=int((self.hight-200)/self.values.N)                              # Calculate distance for placement
                 self.add_photo("Symbol.png",50,80+i*dist)
                 btn.append(Button(self,text=self.__buttom_name(i),bg="red",font="Calibri 12 ",fg="white",relief="raised",command=lambda i=i:self.open_file(btn[i],i)))    
                 btn[i].place(x=100,y=80+(i)*dist)
               


   def __addmore_files(self):
      ''' Function to add more files'''
      # Show warning if they really want it:
      #self.open_file(
      self.values.N+=1
      self.values.png.append(None)
      self.master.destroy()
      root2= Tk()
      window=GUI1(self.values,root2,self.values.N)
      # Check for the size
      
      window=WARNING(root2,1)
      


   def __open_page2(self,values):
      ''' Function to go to page 2'''
            
      if(self.__check_page()):
            self.master.destroy()   # Destroy window
              
            root2= Tk()             # Open new window
            window2=GUI2(values,root2)
      
          
   def __buttom_name(self,i):
       ''' Function to change buttom name''' 
       if(self.values.png[i]!=None):
              name=self.values.png[i].ljust(40)
              name=name[:40]
       else:
              empt="Click to add file "
              name=empt.ljust(30)
              name=name[:20]
       return(name)
          

   def update_btn_text(self,button,text):
          ''' Function to update button'''
          button.config(text=text)
          
   
   def __check_page(self):
            ''' Function to check if all values are correct
            Contains:
                  - Check if self.png is not empty
                  - Check if order is correct
            '''

            
            counter=0                     # dummy values for counting None file names
            last_name_index=0             # Varibale, that has index of last png name
            first_none_index=self.values.N       # Varibale, that has first None index 
            
            for i in range(0,self.values.N):
                  # counts alll none types 
                  if(self.values.png[i]==None):
                        # find idex of first None value
                        if(counter==0):
                              first_none_index=i
                              
                        counter+=1

                  else:
                        last_name_index=i
            # Only None types       
            if(counter>self.values.N-1):
                        window=ERROR(self.master,0)
                        return(False)
            # Wrong order
            if(first_none_index<last_name_index):
                        window=ERROR(self.master,1)
                        return(False)
                        

            
            else:
                  # Set number of final png files
                  self.values.N_png=self.values.N-counter
                  return(True)


 

 ######## GUI2 ################### GUI2 ################### GUI2 ###################         
class GUI2(PARENTGUI):
      ''' Define class for second page'''
      def __init__(self, values,master,saturation_val=70):
          PARENTGUI.__init__(self, values,master)
          self.saturation_val=saturation_val    # Initial value of saturation
          self.value=values                     # names of png
          self.label_img=None                   # Gloabal fotolabel for deleting
          self.executed=False                   # Checks if variable request was executed
          self.saturation=DoubleVar()           # Create slider object 
      

          # Set main Frame and window
          self.__init_window()

      def __init_window(self):
          self.master.title("Binarizing picture")

          # Window parametery
          label_width=20                  
          eingabe_loc=400
          pic_locx=50
          pic_locy=150
  

          # Add slider and Button for adjusting binary value
          showButton=Button(self, text='Show',bg="white",font="Calibri 15 bold",fg="red",relief="raised", command=lambda:self.__update_picture())
          showButton.place(x=350,y=65)
          slider_cont = Scale(self,bg="red",fg="white",font="Calibri 12",from_=0., to=100,resolution=1,relief="raised",length=400, orient=HORIZONTAL,variable=self.saturation)
          slider_cont.set(self.saturation_val)
          slider_cont.place(x=200,y=20)


          # Add photo
          self.__add_binary_photo(self.saturation_val)

          # Add botton finsih and back
          finishButton=Button(self,text="Continue",bg="red",font="Calibri 40 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__open_page3())
          finishButton.place(x=500,y=400)
          backButton=Button(self,text="Back",bg="white",font="Calibri 12 bold",fg="red",relief="raised",command=lambda:self.__open_page1())
          backButton.place(x=50,y=420)




      def __add_binary_photo(self,threshold=0.8,x_max=600,y_max=250):
            ''' Takes
                  threshold := threshold value
                  x_max     := Max value of figure in x direction
                  y_max     := Max value of figure in y direction

               Does
                     Load and binarize first image
                     Rescale image
                     Convert to Tkinter


               Returns
                     A scaled binarized picture at a location
            '''
            
            ## Get name
            name=self.values.png[0]
            ## load image
            img = mpimg.imread("./"+name)

            ## Get filetype 
            filename, file_extentions = os.path.splitext(name)
            # Check if jpeg or png and photo binarize it
            if(file_extentions==".png"):
                  # Adapt threshold to imagetype
                  threshold/=100
                  bin_img=self.picture.binarize_picture_png(img,threshold)
            elif(file_extentions==".jpeg"):
                  # Adapt threshold to imagetype
                  threshold*=2
                  bin_img=self.picture.binarize_picture_jpeg(picture,threshold)
            else:
                  # Wrong format error
                  window=ERROR(self.master,5)
                  
            ## Resize 
            # Calculate the resize value. Later picture will be bigger again
            self.values.size=np.shape(bin_img)              # Set global value size of picture
            x_length=self.values.size[0]                    # Define x length
            y_length=self.values.size[1]                    # Define y length
            scale=min(x_max/x_length,y_max/y_length)        # Find scaling
            if(scale<1):
                  bin_img=self.picture.rescale_image(bin_img,scale)    # Make cmaller for bigger pictures
                  
            if(scale>1):
                  scale=max(x_max/x_length,y_max/y_length)             # Make bigger for smaller picture
                  bin_img=self.picture.rescale_image(bin_img,scale)
     
            ## Display picture
            img = Image.fromarray(bin_img*255)                        # Convert to TKinter format
            photo = ImageTk.PhotoImage(img)                       # Convert to TKinter format
            self.label_img = Label(self,image=photo)
            self.label_img.image=photo
            
            # find location to place it
            posx,posy=self.__put_in_middle(bin_img)
            self.label_img.place(x=posx,y=posy)
            

      def __clear_label_image(self):
          ''' Empties label content'''
          self.label_img.config(image='')
            
      def __put_in_middle(self,bin_img):
            ''' Takes image
                Uses window
                Returns values to place picture
            '''

            x_length,y_length=np.shape(bin_img)

            x_loc=int((self.width-x_length)/2)
            y_loc=int((self.hight-y_length-30)/2)
            return x_loc,y_loc


      def __open_page1(self):
            ''' Function to go to page 2'''         
            self.master.destroy()
            root2= Tk()
            window2=GUI1(self.values,root2)

      def __update_picture(self):
            ''' Gets new saturation value
                Does
                  Empty picture label container
                  
                Returns
                   Updated binarized picture
            '''

            # Set was executed true
            self.executed=True 
            
            # Get value
            val=self.saturation.get()
            # Clear figure
            self.__clear_label_image()
            

            # Show new figure
            self.__add_binary_photo(val)
            

      def __open_page3(self):
            ''' Function to go to page 3'''      
            if(self.__check_page()):
                  self.master.destroy()   # Destroy window
                    
                  root3= Tk()             # Open new window
                  window2=GUI3(self.values,root3,self.saturation.get())

            
      def __next(self):
            if(self.__check_page()==True):
                  self.master.destroy()
         # Now return all values
         
      def __check_page(self):
            # Check if self.saturation was updated
            if(not(self.executed)):
                  window=WARNING(self.master,0)
                  
            
            return(True)

################################### GUI3 #################################### GUI3 ############################
class GUI3(PARENTGUI):
      ''' Define class for second page'''
      def __init__(self, values,master,saturation):
          PARENTGUI.__init__(self, values,master)
          self.value=values               # names of png
          self.saturation_val=saturation  # Saturation
          self.width_stribs_val=2         # Define width of stribe
          self.label_img=None             # Gloabal fotolabel for deleting
          self.stribes=DoubleVar()        # Create slider object
      

          # Set main Frame and window
          self.__init_window()

      def __init_window(self):
          self.master.title("Binarizing picture")

          # Window parametery
          label_width=20                  
          eingabe_loc=400
          pic_locx=50
          pic_locy=150
  

          # Add slider and Button for adjusting binary value
          showButton=Button(self, text='Show',bg="white",font="Calibri 15 bold",fg="red",relief="raised", command=lambda:self.__update_picture())
          showButton.place(x=350,y=65)
          slider_cont = Scale(self,bg="red",fg="white",font="Calibri 12",from_=0, to=10,resolution=1,relief="raised",length=400, orient=HORIZONTAL,variable=self.stribes)
          slider_cont.set(self.width_stribs_val)
          slider_cont.place(x=200,y=20)


          # Add photo
          self.__add_stribe_photo(self.width_stribs_val)

          # Add botton finsih and back
          finishButton=Button(self,text="Continue",bg="red",font="Calibri 40 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:__open_page3())
          finishButton.place(x=500,y=400)
          backButton=Button(self,text="Back",bg="white",font="Calibri 12 bold",fg="red",relief="raised",command=lambda:self.__open_page2(self.values))
          backButton.place(x=50,y=420)




      def __add_stribe_photo(self,s_width,x_max=600,y_max=250):
            ''' Takes
                  s_width := width of the stribes
                Uses
                  N       := Number of png files
                  size    := size of first file 
            '''            
            pattern=self.picture.create_stripes(self.values.size,self.values.N_png,s_width)

            ## Resize 
            # Calculate the resize value. Later picture will be bigger again
            x_length,y_length=np.shape(pattern)
            scale=min(x_max/x_length,y_max/y_length)        # Find scaling
            if(scale<1):
                  pattern=self.picture.rescale_image(pattern,scale)    # Make cmaller for bigger pictures
                  
            if(scale>1):
                  scale=max(x_max/x_length,y_max/y_length)             # Make bigger for smaller picture

                  pattern=self.picture.rescale_image(pattern,scale)
     
            ## Display picture
            img = Image.fromarray(pattern*255)                    # Convert to TKinter format
            photo = ImageTk.PhotoImage(img)                       # Convert to TKinter format
            self.label_img = Label(self,image=photo)
            self.label_img.image=photo
            
            # find location to place it
            posx,posy=self.__put_in_middle(pattern)
            self.label_img.place(x=posx,y=posy)

            

      def __clear_label_image(self):
          ''' Empties label content'''
          self.label_img.config(image='')
            
      def __put_in_middle(self,bin_img):
            ''' Takes image
                Uses window
                Returns values to place picture
            '''

            x_length,y_length=np.shape(bin_img)

            x_loc=int((self.width-x_length)/2)
            y_loc=int((self.hight-y_length-30)/2)
            return x_loc,y_loc


      def __open_page2(self):
            ''' Function to go to page 2'''         
            self.master.destroy()
            root2= Tk()
            window2=GUI2(values,root2,self.saturation)

      def __update_picture(self):
            ''' Gets new saturation value
                Does
                  Empty picture label container
                  
                Returns
                   Updated binarized picture
            '''
            
            # Get value
            val=int(self.stribes.get())
            print(val)
            # Clear figure
            self.__clear_label_image()
            

            # Show new figure
            self.__add_stribe_photo(val)
            

            
      def __next(self):
            if(self.__check_page()==True):
                  self.master.destroy()
         # Now return all values
         
      def __check_page(self):
            return(True)



######## WARNING ################### WARNING ################### WARNING ###################
              
class WARNING(SIDESIDE):
        ''' Class for warnings'''
        def __init__(self, original,Nr):
              """Constructor"""
              SIDESIDE.__init__(self, original)
              self.Nr=Nr
              self.decision=False
              self.main.title("Warning Nr. "+ str(self.Nr))#
              T = Text(self.main, height=10, width=45)
              T.place(x=20,y=20)
              ok=self.__warning_handler(T)
              backbtn = Button(self, text="Back", bg="red",width=8,font="Calibri 20",fg="white",relief="raised",command=lambda:self.__back()).place(x=20,y=240)
              okbtn = Button(self, text="OK", bg="white",width=6,font="Calibri 15",fg="red",relief="raised",command=lambda:self.__ok()).place(x=270,y=245)

        def __back(self):           
              self.main.destroy()
              self.show()
              
        def __ok(self):
              self.decision=True
              self.main.destroy()
              self.show()

        def __return_decision(self):
             return self.decision
              
            
        def __warning_handler(self,T):
              if(self.Nr==0):
                    text="Caution. Default saturation was used"
                    T.insert(END,text)
                    return 0  
                    
              if(self.Nr==1):
                    text="The best number for this illusion is between 2 and 5."
                    T.insert(END,text)
                    return 0                                    
              else:
                    text="Unbekannter error. \nContact Marius Neugschwender"
                    T.insert(END,text)
                    #unknown erro pleas contact     


              



######## ERROR ################### ERROR ################### ERROR ###################
              
class ERROR(SIDESIDE):
        ''' Class for errors'''
        def __init__(self, original,Nr):
              """Constructor"""
              SIDESIDE.__init__(self, original)
              self.Nr=Nr
             
              self.main.title("Error Nr. "+ str(self.Nr))#
              T = Text(self.main, height=10, width=45)
              T.place(x=20,y=20)
              ok=self.__error_handler(T)
              backbtn = Button(self, text="Back", bg="red",width=10,font="Calibri 20",fg="white",relief="raised",command=lambda:self.__back()).place(x=100,y=220)

        def __error_handler(self,T):

              
              if(self.Nr==0):
                    text="You have to choose at least two pictures"
                    T.insert(END,text)
                    return 0            
              if(self.Nr==1):
                    text="Don't leave blanck sides \n"
                    T.insert(END,text)
                    return 0


              if(self.Nr==2):
                    text="Keine Dateien ausgewählt. \nBitte Dateien auswählen!"
                    T.insert(END,text)
                    return 0
              if(self.Nr==3):
                    text="Pictures need to have the same size!"
                    T.insert(END,text)
                    return 0
              if(self.Nr==4):
                    text="Bitte Titel des KT's angeben!"
                    T.insert(END,text)
                    return 0
              if(self.Nr==5):
                    text="Wrong format, only png and jpeg are accepted"
                    T.insert(END,text)
                    return 0  
                                                  
              else:
                    text="Unknown error. \nPlease contact Marius Neugschwender"
                    T.insert(END,text)
                    #unknown erro pleas contact     
             
        def __back(self):           
              self.main.destroy()
              self.show()
              
###############PICTURE CLASS  #################################################################


class PICTURE():
      ''' Class to control the all picture related things
      and make the moire ilussion, after the user has loaded and made the inputs.
      '''
      def __init__(self):
            #define basic initial properties
            self.s_width=4                # Stribe width

      
      # helper functions
      def rgb2gray(self,rgb):
          return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

      def binarize_picture_jpeg(self,img,threshold=130):
          ''' Takes:   Picture object
              Creates: Greyscale -> binarixed picture
          '''
      
          # Convert to binary 
          gray = self.rgb2gray(img)
          bin_img=1.0 * (gray > threshold)
          return bin_img


      def binarize_picture_png(self,img,threshold=0.7):
          ''' Takes:   Picture object
              Creates: Greyscale -> binarixed picture 
          '''
          # Load picture
          #img = mpimg.imread(name)

          # Convert to binary 
          gray = self.rgb2gray(img)
          bin_img=1.0 * (gray > threshold)
          return bin_img

      def one_to_zero(self,A):
          A=A-1
          A*=(-1)
          return A

      def simulate(self,pattern,output,N=100):
          animation_pic=[]
          for i in range(0,N):   
              bild=self.one_to_zero(pattern)+output
              bild=bild>0.5
              bild=np.array(bild)
              pattern=np.roll(pattern,self.s_width)
              animated_bild=plt.imshow(bild,animated=True)
              animation_pic.append([animated_bild])

          return animation_pic
          

      def length_check(self,img):
          size=np.shape(img)
          return size

      def create_stripes(self,size,N,s_width=2):
          # Create array
          N_s=np.zeros([size[0],N*s_width])
          # Fill with ones
          N_s[:,0:s_width]=np.ones([size[0],s_width])

          # multiply
          pattern=np.tile(N_s,int(np.floor(size[1]/(N*self.s_width))))
          rest_array=np.zeros([size[0],size[1]%(N*self.s_width)])
          pattern=np.concatenate((pattern,rest_array),axis=1)

          return pattern
          
                                  
      def rescale_image(self,bin_img,imgScale=1):
          ''' Takes
                  Rescales binarized image only
              Retruns
                  Resized picture'''
          height, width = bin_img.shape
          newX,newY = bin_img.shape[1]*imgScale, bin_img.shape[0]*imgScale
          newimg = cv2.resize(bin_img,(int(newX),int(newY)))
          return newimg                  
                   

      def main(self):
          # Set names of png pictures
          #picture_names=["bar1.png","bar2.png","bar3.png","bar4.png"]   
          #picture_names=["me1.jpeg","me2.jpeg","me3.jpeg","me4.jpeg"]
          picture_names=["1.png","2.png","3.png","4.png"]   
          #picture_names=["text1.png","text2.png","text3.png","text4.png"]  
          #picture_names=["test.png"]

          # Get type of object
          filename, file_extentions = os.path.splitext(picture_names[0]) 
          N=len(picture_names)
          # Loop over all pictures
          for i,picture in enumerate(picture_names):
              
              
              # Load and convert picture
              if(file_extentions==".png"):
                  bin_img=self.binarize_picture_png(picture)
              elif(file_extentions==".jpeg"):
                  bin_img=self.binarize_picture_jpeg(picture)
              else:
                  raise("File format not supported, please use png oder jpeg")
                  

              # Get length
              size=self.length_check(bin_img)


              
              # Load each picture check size and save size, if size is not the same show error
              # Create test pattern only one tyme

              if (i==0):
                  # Create pattern
                  print("Create pattern \n")
                  pattern=self.create_stripes(size,N,self.s_width)
                  # Save pattern
                  imageio.imsave('./Output/'+filename+'_pattern42'+file_extentions, pattern)

                  # Create output
                  output=np.zeros(size)
                  print("Create Moire pictue \n \n")
              else:
                  pattern=np.roll(pattern,self.s_width)

          
              moire=self.one_to_zero(bin_img)*(pattern)
              output+=moire
          
          output=output>0.5
          output=np.array(output)
          imageio.imsave('./Output/'+filename+'_moire42'+file_extentions, one_to_zero(output))

          # Simulate
          fig = plt.figure()
          ims=self.simulate(pattern,output)
          ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True,
                                          repeat_delay=1000)
          plt.show()                               
#MAINGUI()
def main():
      # Make Tknter window and get values
      root=Tk()
      values=VALUES()
      Window=GUI1(values,root)
      root.mainloop()
      print(values.return_values())

      # here Stefan ... make Powerpoint

if __name__ == "__main__":
    main()
