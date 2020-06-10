# Using python 3.6
from tkinter import *                                                   #Standart                        
from PIL import Image,ImageTk                                           ### Instalation needed
from tkinter.filedialog import askopenfilenames,askopenfilename         # Comes with TK inter
import subprocess                                                       # Standart      
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg         # pseudostandart
from scipy.ndimage.interpolation import rotate                          # Scipy needs to be added
# For Moire
import numpy as np                              # Array handling
import matplotlib.image as mpimg                # Load image
import imageio                                  # Save image without yellow               
import cv2                                      # Scale image
import os                                       # Get fileformart
import matplotlib.animation as animation        # Animation of Moire


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
          self.master=master                                 # main window
          self.picture=PICTURE()                             # Class for Fotos
          self.values=values
          # Define screen constants
          self.width=800            # Window length
          self.hight=500            # Window hight
          self.to_big=3300          # Recommended upper limit for picture
          self.to_small=30          # Recommended lowelimit for picture
          #set background fixed to locate objects with place (x=x,y=y)
          self.pack(fill=BOTH,expand=1)
          self.master.geometry(str(self.width)+"x"+str(self.hight))
          self.master.resizable(0, 0)

          # add menu bar
          self.__menu()      
                       
            
                  
      def __menu(self):
          ''' Function to create menu bar'''
          # creating a menu instance
          menu = Menu(self.master)
          self.master.config(menu=menu)

          # create the file object
          file = Menu(menu)
          file.add_command(label="Exit", command=self.client_exit)
          #file.add_command(label="Open File", command=self.open_file)
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
          load =Image.open(name)
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
      ''' Class to store values of all the relevant information. 
      All other classes will inherit this class ti change the values directely
      '''
            
      def __init__(self,N=6,png=[],size=[0,0],N_png=0,output_loc="./Output",w_stribes=5,saturation=70):
          self.N=N                                    # Default numbers button
          self.png=[None]*self.N                      # Create Empty list for png
          self.size=size                              # Size of first loaded picture
          self.N_png=N_png                            # Number of loaded png
          self.output_loc=output_loc                  # Output location
          self.width_stribs_val=w_stribes             # Width of stribe
          self.saturation_val=[saturation]            # Saturation level for each picture binarizing
          self.gif_name='/animated-moire.gif'         # Name of gif
          self.moire_name='/moire.png'                # Name of Moire
          self.pattern_name='/pattern.png'            # Name of pattern
          self.pattern=np.zeros([1,1])                # Array to store pattern
          self.moire=np.zeros([1,1])                  # Aray to store moire images for gif
          

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
          self.N=self.values.N      # Default numbers button
          self.png=[None]*self.N    # Create Empty list for Powerpoints             
          self.saturation=80
          self.pattern_width=10

   
######## GUI1 ################### GUI1 ################### GUI1 ###################
class GUI1(PARENTGUI):
   ''' Class for page 1'''
   def __init__(self, values,master=None,N=7):
          PARENTGUI.__init__(self,values,master)
          # Set main Frame and window
          self.__init_window()


         

   def __init_window(self):
          self.master.title("Loading files")
              
          # Add botton merge
          mergeButton=Button(self,text="Continue",bg="red",font="Calibri 40 bold",fg="white",relief="raised",command=lambda:self.__open_page2())
          mergeButton.place(x=450,y=400)
          
          # Add botton more Files
          addmoreFilesButton=Button(self,text="Add more files",bg="white",font="Calibri 20 bold",fg="red",relief="raised",command=lambda:self.__addmore_files())
          addmoreFilesButton.place(x=450,y=350)


          # Automised N buttoms with unambiguous identity due to list
          btn=[]
          for i in range(0,self.values.N):
                 dist=int((self.hight-120)/self.values.N)         # Calculate distance for placement
                 self.add_photo("./AppData/Symbol.png",50,50+i*dist)
                 btn.append(Button(self,text=self.__buttom_name(i),bg="red",font="Calibri 12 ",fg="white",relief="raised",command=lambda i=i:self.open_file(btn,i)))    
                 btn[i].place(x=100,y=50+(i)*dist)
               


   def __addmore_files(self):
      ''' Function to add more files'''
      # Show warning if they really want it:
      #self.open_file(
      self.values.N+=1
      self.values.png.append(None)
      self.values.saturation_val.append(self.values.saturation_val[0])
      self.master.destroy()
      root2= Tk()
      window=GUI1(self.values,root2,self.values.N)
      # Check for the size
      
      window=WARNING(root2,1)
      

   def open_file(self,button_list,i):
           ''' Function to open only png files
               Takes:
                         - Buttom event
               Returns:
                         - name of selceted Powerpoint
                         - adds powertpoint to list
            '''
           # Open file
           try:
                 names = askopenfilenames(parent=self.master,initialdir = "./Images",filetypes =(("Images", "*.png"),("Images","*.jpeg")),
                                        title = "Choose a file."
                                        )
           except:
                 window=ERROR(self.master,7)

 
           # Check if nothing was selectet
                 # Do not change self.png
                 # Set buttom to deflaut value
           if(names==()):
                  empt="Click to add file "
                  name=empt.ljust(30)
                  bname=name[:20]
           
           # Multiple files where selected
           else:
                 for j,name in enumerate(names):
                        bname=(self.relative_name(str(name)))
                        self.values.png[i+j]=bname
                        bname=bname.ljust(40)
                        bname=bname[:40]

                        # Check the input is correct
                        self.update_btn_text(button_list[i+j],bname)
                        self.__check_image_properties(i+j,button_list[i+j])
                        self.__buttom_name(i+j)



                        
   def __check_image_properties(self,i,button):
           ''' Takes
                  i := index button
            Does
               loads image
               checks if loaded image has same dimesion like excisting ones
               checks size
               saves values in global class values
            '''

           
           # Load image to check properties
           img = mpimg.imread("./"+self.values.png[i])
           x,y,z=np.shape(img)
           size=np.array([x,y])
           
           # Set image properties from first file
           if(i==0):
                 # Set global value size
                 self.values.size=size
                 
           # check for same size like the first one
           else:   
                 if(size[0]!=self.values.size[0] or size[1]!=self.values.size[1]):
                     # Reset values entry and button
                     self.values.png[i]=None
                     text="Click to add file "
                     text=text.ljust(30)
                     text=text[:20]
                     self.update_btn_text(button,text)
                     # Show error
                     window=ERROR(self.master,3)

                     
      

           # Show warning if file is probably to big
           if(max(size)>self.to_big):
                    window=WARNING(self.master,2)

           # Show warning if probably to small
           if(min(size)<self.to_small):
                    window=WARNING(self.master,3)


           # delete image again or save as global
           del(img)

           

   def __open_page2(self):
      ''' Function to go to page 2'''
            
      if(self.__check_page()):
            self.master.destroy()   # Destroy window
              
            root2= Tk()             # Open new window
            window2=GUI2(self.values,root2)
      
          
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
            if(counter>self.values.N-2):
                        window=ERROR(self.master,0)
                        return(False)
            # Wrong order
            if(first_none_index<last_name_index):
                        window=ERROR(self.master,1)
                        return(False)
                        

            
            else:
                  # Set number of final png files
                  self.values.N_png=self.values.N-counter
                  # Update all numbers related to file number
                  self.values.saturation_val=self.values.saturation_val*self.values.N_png
                  return(True)


 

 ######## GUI2 ################### GUI2 ################### GUI2 ###################         
class GUI2(PARENTGUI):
      ''' Define class for second page'''
      def __init__(self, values,master):
          PARENTGUI.__init__(self, values,master)
          self.value=values                     # names of png
          self.label_img=None                   # Gloabal fotolabel for deleting
          self.executed=False                   # Checks if variable request was executed
          self.saturation=DoubleVar()           # Create slider object
          self.pic_pointer=0                    # Indixes of displayed picture
          self.warning_acivation=True             # Display warning only once
      

          # Set main Frame and window
          self.__init_window()

      def __init_window(self):
          ''' Function to set up window'''
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
          slider_cont.set(self.values.saturation_val[0])
          slider_cont.place(x=180,y=20)

          # Add Help Button
          helpButton=Button(self,text='?',bg="white",font="Calibri 12 bold",fg="black",relief="raised",command=lambda:self.__help())
          helpButton.place(x=590,y=28)

          # Add photo
          self.__add_binary_photo()

          # Add button to show nex picture
          nextpicButton=Button(self,text="Next picture",bg="red",font="Calibri 20 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__next_pic())
          nextpicButton.place(x=290,y=415)
          
          # Add botton finsih and back
          finishButton=Button(self,text="Continue",bg="red",font="Calibri 14 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__open_page3())
          finishButton.place(x=650,y=420)
          backButton=Button(self,text="Back",bg="white",font="Calibri 12 bold",fg="red",relief="raised",command=lambda:self.__open_page1())
          backButton.place(x=50,y=420)




      def __add_binary_photo(self,x_max=600,y_max=250):
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
            name=self.values.png[self.pic_pointer%self.values.N_png]
            ## load image
            img = mpimg.imread("./"+name)

            # Binarize img
            bin_img=self.__binarize_img(img,self.values.saturation_val[self.pic_pointer%self.values.N_png],name)
            
            ## Resize 
            self.values.size=np.shape(bin_img)              # Set global value size of picture

            bin_img=self.__resize_bin(bin_img)              # Resize
            
            ## Display picture
            img = Image.fromarray(bin_img*255)              # Convert to TKinter format
            photo = ImageTk.PhotoImage(img)                 # Convert to TKinter format
            self.label_img = Label(self,image=photo)
            self.label_img.image=photo
            
            # find location to place it
            posx,posy=self.__put_in_middle(bin_img)
            self.label_img.place(x=posx,y=posy)
            

      def __clear_label_image(self):
          ''' Empties label content'''
          self.label_img.config(image='')

      def __help(self):
            help_site=HELP(self.master,0)
            
      def __put_in_middle(self,bin_img):
            ''' Takes image
                Uses window
                Returns values to place picture
            '''

            x_length,y_length=np.shape(bin_img)

            x_loc=int((self.width-y_length)/2)
            y_loc=int((self.hight-x_length-5)/2)
            return x_loc,y_loc

      def __next_pic(self):
            ''' Function to increasi image pointer to show next picture'''
            
            if(self.pic_pointer>=self.values.N_png-1 and self.warning_acivation):  # Show only once if all pictures have been set
                  window=WARNING(self.master,5)
                  self.warning_acivation=False
                  
            self.pic_pointer+=1
            self.__clear_label_image()    # Clear screen
            self.__add_binary_photo()     # Add new picture

            
      def __resize_bin(self, bin_img,x_max=600,y_max=280):
            ''' Resizes binary images
                Takes
                  image
                Returns
                  resized image
            '''
            y_length,x_length=np.shape(bin_img)
            scale=max(x_max/x_length,y_max/y_length)                   # Find scaling
            if(scale<1):
                  scale=min(x_max/x_length,y_max/y_length)
                  re_img=self.picture.rescale_image(bin_img,scale)    # Make cmaller for bigger pictures
                  
            if(scale>1):
                  scale=max(x_max/x_length,y_max/y_length)             # Make bigger for smaller picture

                  re_img=self.picture.rescale_image(bin_img,scale)

            return re_img

      def __open_page1(self):
            ''' Function to go to page 2'''         
            self.master.destroy()
            root2= Tk()
            window2=GUI1(self.values,root2)

      def __binarize_img(self,img,threshold,name):
            ''' Binarizes img uses picture class'''
            ## Get filetype 
            filename, file_extentions = os.path.splitext(name)
            # Check if jpeg or png and photo binarize it
            if(file_extentions==".png"):
                  # Adapt threshold to imagetype
                  threshold/=100
                  bin_img=self.picture.binarize_picture_png(img,threshold)
            elif(file_extentions==".jpeg"):
                  # Adapt threshold to imagetype
                  threshold+=50
                  threshold*=1.2
                  threshold=max(threshold,0)
                  
                  bin_img=self.picture.binarize_picture_jpeg(img,threshold)
            return bin_img

            
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

            # Write saturation value in values class
            self.values.saturation_val[self.pic_pointer%self.values.N_png]=val

            # Choose last value as default for Rest
            if(self.pic_pointer<self.values.N_png-1):
                  for i in range(self.pic_pointer,self.values.N_png):
                        self.values.saturation_val[i]=self.values.saturation_val[self.pic_pointer]
                        
            
            # Clear figure
            self.__clear_label_image()
            

            # Show new figure
            self.__add_binary_photo(val)
            

      def __open_page3(self):
            ''' Function to go to page 3'''      
            if(self.__check_page()):
                  self.master.destroy()   # Destroy window
                    
                  root3= Tk()             # Open new window
                  window2=GUI3(self.values,root3)

         
      def __check_page(self):             
            return(True)

################################### GUI3 #################################### GUI3 ############################
class GUI3(PARENTGUI):
      ''' Define class for second page'''
      def __init__(self, values,master):
          PARENTGUI.__init__(self,values,master)
          self.value=values               # names of png
          self.label_img=None             # Gloabal fotolabel for deleting
          self.stribes=DoubleVar()        # Create slider object
          self.pattern=np.zeros([1,1])    # Pattern object
          self.pic_pointer=0              # Poiter to adress current image
      

          # Set main Frame and window
          self.__init_window()

      def __init_window(self):
          ''' Funtion to initialize visible screen'''
          self.master.title("Choose stips")

          # Window parametery
          label_width=20                  
          eingabe_loc=400
          pic_locx=50
          pic_locy=150
  

          # Add slider and Button for adjusting binary value
          showButton=Button(self, text='Show',bg="white",font="Calibri 15 bold",fg="red",relief="raised", command=lambda:self.__update_picture())
          showButton.place(x=350,y=65)
          slider_cont = Scale(self,bg="red",fg="white",font="Calibri 12",from_=1, to=10,resolution=1,relief="raised",length=400, orient=HORIZONTAL,variable=self.stribes)
          slider_cont.set(self.values.width_stribs_val)
          slider_cont.place(x=180,y=20)

          # Add Help Button
          helpButton=Button(self,text='?',bg="white",font="Calibri 12 bold",fg="black",relief="raised",command=lambda:self.__help())
          helpButton.place(x=590,y=28)



          # Add photo
          self.__add_stribe_photo()


          # Add button to show nex picture
          '''
            Optional in testcase it did not make much sense!
            nextpicButton=Button(self,text="Next picture",bg="red",font="Calibri 20 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__next_pic())
            nextpicButton.place(x=290,y=415)
          '''
                
          # Add botton finsih and back
          finishButton=Button(self,text="Continue",bg="red",font="Calibri 14 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__show_preview())
          finishButton.place(x=650,y=420)
          backButton=Button(self,text="Back",bg="white",font="Calibri 12 bold",fg="red",relief="raised",command=lambda:self.__open_page2())
          backButton.place(x=50,y=420)




      def __add_stribe_photo(self,x_max=600,y_max=250):
            ''' Takes
                  s_width := width of the stribes
                Uses
                  N       := Number of png files
                  size    := size of first file
            '''
            ## Make moire
            moire=self.__moire(self.values.width_stribs_val)

            ## Resize
            moire=self.__resize_bin(moire)
     
            ## Display picture
            img = Image.fromarray(moire*255)                    # Convert to TKinter format
            photo = ImageTk.PhotoImage(img)                     # Convert to TKinter format
            self.label_img = Label(self,image=photo)
            self.label_img.image=photo
            
            # find location to place it
            posx,posy=self.__put_in_middle(moire)
            self.label_img.place(x=posx,y=posy)


      def __next_pic(self):
            ''' Function to increase image pointer to show next picture '''
            
         
            self.pic_pointer+=1
            self.__clear_label_image()    # Clear screen
            self.__add_stribe_photo()     # Add new picture 

      def __moire(self,val_width):
            ''' Takes
                  val_width     := Input of usuer
                Returns
                  Moire picture
            '''

            
            s_width_pix=self.__stribe_sizer(self.values.width_stribs_val)            # Value of one corresonds to N pixels
            # Load image
            name=self.values.png[self.pic_pointer%self.values.N_png]
            img = mpimg.imread("./"+name)

            # Binarize img
            bin_img=self.__binarize_img(img,self.values.saturation_val[self.pic_pointer%self.values.N_png],name)
            
            
            # Create pattern
            pattern=self.picture.create_stripes(self.values.size,self.values.N_png,s_width_pix)

            # Save pattern object
            self.values.pattern=pattern

            # Create Moire
            moire=moire=self.picture.one_to_zero(bin_img)*(pattern)     # Create Moire
            moire=self.picture.one_to_zero(moire)                       # Invert because 1 is black
            return moire
            

      def __stribe_sizer(self,N_s):
            ''' Calculates a sensful range of stribe_width according to the picture size

                  Input         Number of stribs
                  1             100             N_stribes[0]
                  2             75              N_stribes[1]
                  .
                  .
                  .
                  10             6              N_stribes[9]

            '''
            found=False                                     # Value to display if not found
            N_stribes=np.array([2,4,5,10,15,25,40,60,80,100])      # Define stribes for value
            for i,val in enumerate(N_stribes):
                  if(i+1==N_s):
                        s_width_pix=self.__width_handler(val)
                        found=True
                        return s_width_pix
            if(not(found)):
                  window=ERROR(self.master,19)

            
            
      def __binarize_img(self,img,threshold,name):
            ''' Binarizes img uses picture class'''
            ## Get filetype 
            filename, file_extentions = os.path.splitext(name)
            # Check if jpeg or png and photo binarize it
            if(file_extentions==".png"):
                  # Adapt threshold to imagetype
                  threshold/=100
                  bin_img=self.picture.binarize_picture_png(img,threshold)
            elif(file_extentions==".jpeg"):
                  # Adapt threshold to imagetype
                  # Adapt threshold to imagetype
                  threshold+=50
                  threshold*=1.2
                  threshold=max(threshold,0)
                  bin_img=self.picture.binarize_picture_jpeg(img,threshold)
            return bin_img
      
      
      def __help(self):
            help_site=HELP(self.master,1)

      def __width_handler(self,N_s):
            '''Takes
                  N := Number of stribes
               Returns
                  s_wdth:= best estimaton of s_width for N stribes given a photo with size(nxm)
            '''
            x_size=self.values.size[1]                                  # !!! np.shape definition x,y,z=np.shape() x is the vertical and y the horizontal
            # calculate s_width
            ''' One cell contains N_s patern lik this:
            w1 ... ws_width | w1 .... ws_width | ...N_png times... |  w1 ... ws_width
            -> s_width=x_size/(N_s*self.values.N_png)
            '''
            s_width=int(round(x_size/(N_s*self.values.N_png)))     
            return s_width

            
      def __resize_bin(self, bin_img,x_max=600,y_max=300):
            ''' Resizes binary images
                Takes
                  image
                Returns
                  resized image
            '''
            # Find scaling
            y_length,x_length=np.shape(bin_img)
            scale=max(x_max/x_length,y_max/y_length)                   # Find scaling
            if(scale<1):
                  scale=min(x_max/x_length,y_max/y_length)
                  re_img=self.picture.rescale_image(bin_img,scale)    # Make cmaller for bigger pictures
                  
            if(scale>1):
                  scale=max(x_max/x_length,y_max/y_length)             # Make bigger for smaller picture

                  re_img=self.picture.rescale_image(bin_img,scale)
            return re_img





      def __clear_label_image(self):
          ''' Empties label content'''
          self.label_img.config(image='')


          
            
      def __put_in_middle(self,bin_img):
            ''' Takes image
                Uses window
                Returns values to place picture
            '''

            x_length,y_length=np.shape(bin_img)

            x_loc=int((self.width-y_length)/2)
            y_loc=int((self.hight-x_length+15)/2)
            return x_loc,y_loc


      


      def __open_page2(self):
            ''' Function to go to page 2'''         
            self.master.destroy()
            root2= Tk()
            window2=GUI2(self.values,root2)



            

      def __update_picture(self):
            ''' Gets new saturation value
                Does
                  Empty picture label container
                  
                Returns
                   Updated binarized picture
            '''

            # Get value
            val=int(self.stribes.get())

            # Upate value in values class
            self.values.width_stribs_val=val
            
            # Clear figure
            self.__clear_label_image()        

            # Show new figure
            self.__add_stribe_photo(val)

      def __save_picturs(self):
            ''' Creates the sliced moire pictues form pattern and saves it 


            '''

            # Create Output variable
            output=np.zeros(self.values.size)
            
            for i in range(0,self.values.N_png):
               # Load image
               name=self.values.png[i]
               img = mpimg.imread("./"+name)

               # Binarize img
               bin_img=self.__binarize_img(img,self.values.saturation_val[i],name)
    
               # Save load and save pattern
               if(i==0):
                     # Get pattern
                     pattern=self.values.pattern
                     # Save pattern
                     print("Created pattern")
                     imageio.imsave(self.values.output_loc+self.values.pattern_name, pattern)
                     
               # Don't save pattern again
               else:
                     pattern=np.roll(pattern,self.__stribe_sizer(self.values.width_stribs_val))    # Roll pattern to make different pictures visible maybe better save other varibale :)

               
               # Create Moire
               moire=self.picture.one_to_zero(bin_img)*(pattern)           # Create Moire
               # Add to output
               output+=moire
               

            # Binarize again  // Overlaps means values higher then 1
            output=output>0.5

            # Save output
            self.values.moire=output
            
            output=self.picture.one_to_zero(output)                             # Invert because 1 is black
            # Save  image
            print("Created Moire")
            imageio.imsave(self.values.output_loc+self.values.moire_name, output)

            
      def __show_preview(self):

         # Empty output folder
         self.__delete_all_files()

         # Save images and pattern
         self.__save_picturs()
               
         # Make and save gif animation
         self.__gif_animation()

         #self.__open_page4()

      
         if(self.__check_page()):
            self.master.destroy()   # Destroy window
              
            root2= Tk()             # Open new window
            window3=GUI4(self.values,root2)

      

      def __gif_animation(self,loop=0,N_steps=2,roll_fac=3):
            ''' Takes
                  duration:= Time to diyplay arach file
                  loop    := Number of times to loop the gif sequence
                  N_steps := Number of steps in s_width
                  roll_fac:= Factor of how far to roll
                  
                Creates gif in Output file
             '''
            
            # create a tuple of display durations, one for each frame
            duration = self.__best_duration(N_steps)

            # load all the static images into a list
            gif_filepath = self.values.output_loc+self.values.gif_name

            # Create list of images
            images=[]
            # Define steps for virtual rolling of image
            N_roll=N_steps*self.values.N_png

            
            # Calculate rollsize
            roll_size=max(1,int(self.__stribe_sizer(self.values.width_stribs_val)/N_steps))
            
            # Loop
            for i in range(0,int(N_roll*roll_fac)):  
               # Save load and save pattern
               if(i==0):
                     # Get pattern
                     pattern=self.values.pattern
                     
               # Don't save pattern again
               else:
                     pattern=np.roll(pattern,roll_size)                       # Roll pattern to make different pictures visible maybe better save other varibale :)
               # add pattern to output
               image=self.values.moire+self.picture.one_to_zero(pattern)
               image=self.picture.one_to_zero(image)
               image = Image.fromarray(image*255)           
               images.append(image)

            # save as an animated gif
            gif = images[0]
            gif.save(fp=gif_filepath, format='gif', save_all=True, append_images=images[1:],duration=duration,loop=loop)

            # Verify that the number of frames in the gif equals the number of image files and durations
            if(not(Image.open(gif_filepath).n_frames == len(images))):
               window=ERROR(self.master,6)

            print("Created GIF")
            
      def __best_duration(self, N_steps=4,rep_time=0.5):
            duration=int((1000*rep_time)/N_steps)          # Calculate best duration and convert to ms
            return duration      

      def __delete_all_files(self):
            ''' Function deletes gif and png files in output dictionary'''
            
            # delete old png files
            filelist = [ f for f in os.listdir(self.values.output_loc) if f.endswith(".png") ]
            for f in filelist:
                os.remove(os.path.join(self.values.output_loc, f))
                
            # Delete old gif list
            filelist = [ f for f in os.listdir(self.values.output_loc) if f.endswith(".png") ]
            for f in filelist:
                os.remove(os.path.join(self.values.output_loc, f))

         
      def __check_page(self):
            return(True)

      
      
############################### PAGE 4 ################################## PAGE 4
class GUI4(PARENTGUI):
      ''' Define class for second page'''
      def __init__(self, values,master=None,N=5):
                PARENTGUI.__init__(self,values,master)
                ''' Function to add more files'''
                #self.open_file(
                self.value=values               # all relevant values
                self.x_pos=90                  # Position x text
                self.y_pos=40                   # Position y text
                self.hight=6                    # Hight text in lines
                self.width=42                   # Width Text lines

                self.posx_b=280                 # Position Button y
                self.posy_b=250                 # Position Button y

                self.text_inst="\n"+"             A simulated GIF should open soon.\n"+   "   Press 'Reality check' to simulate a realistic GIF! \n\n                      Have a nice day"

                # Set main Frame and window
                self.__init_window()

      def __init_window(self):
                self.master.title("Review data")

                # Window parametery
                label_width=20                  
                eingabe_loc=400
                pic_locx=50
                pic_locy=160

                # Add gif
                self.__open_gif()


                # Final instructions
                T_i = Text(self.master, height=self.hight, width=self.width,font="Calibri 18",bg="white")
                T_i.insert(END, self.text_inst)
                T_i.place(x=self.x_pos,y=self.y_pos)



                  

                # Show again button
                #showButton=Button(self, text='Show again',bg="white",font="Calibri 25 bold",fg="red",relief="raised", command=lambda:self.__show_gif_again())
                #showButton.place(x=self.posx_b,y=self.po    sy_b)

                realityButton=Button(self,text="Reality check",bg="white",font="Calibri 25 bold",fg="red",relief="raised",command=lambda:self.__simulate_human())
                realityButton.place(x=self.posx_b,y=self.posy_b)

                # Add Help Button
                helpButton=Button(self,text='?',bg="white",font="Calibri 12 bold",fg="black",relief="raised",command=lambda:self.__help())
                helpButton.place(x=570,y=262)

        

                # Add botton finsih and back
                finishButton=Button(self,text="Finish",bg="red",font="Calibri 40 bold",fg="white",activebackground="white",highlightbackground="white",relief="raised",command=lambda:self.__finish())
                finishButton.place(x=520,y=400)
                backButton=Button(self,text="Back",bg="white",font="Calibri 12 bold",fg="red",relief="raised",command=lambda:self.__open_page3())
                backButton.place(x=340,y=420)




      def __stribe_sizer(self,N_s):
            ''' Calculates a sensful range of stribe_width according to the picture size

                  Input         Number of stribs
                  1             100             N_stribes[0]
                  2             75              N_stribes[1]
                  .
                  .
                  .
                  10             6              N_stribes[9]

            '''
            found=False                                     # Value to display if not found
            N_stribes=np.array([2,4,5,10,15,25,40,60,80,100])      # Define stribes for value
            for i,val in enumerate(N_stribes):
                  if(i+1==N_s):
                        s_width_pix=self.__width_handler(val)
                        found=True
                        return s_width_pix
            if(not(found)):
                  window=ERROR(self.master,19)               


      def __simulate_human(self,loop=0,N_steps=2,roll_fac=3,max_deg=3):
                 ''' Simulates imperfect rolling to get the expected result
                        Takes:
                              duration:= Time to diyplay arach file
                              loop    := Number of times to loop the gif sequence
                              N_steps := Number of steps in s_width
                              roll_fac:= Factor of how far to roll
                            max_degree := Maximum change of degree
                        Returns
                            gif simulation with missmatched pattern
                 '''

                 ''' Predefinition and calculation of things'''

                 # GIF
                 # create a tuple of display durations, one for each frame
                 duration = self.__best_duration(N_steps)

                 # load all the static images into a list
                 gif_filepath = self.values.output_loc+self.values.gif_name

                 # Create list of images
                 images=[]
                 # Define steps for virtual rolling of image
                 N_roll=N_steps*self.values.N_png

                 # ANGULAR MISMATCH
                 roll_size=max(1,int(self.__stribe_sizer(self.values.width_stribs_val)/N_steps))   # Calculate rollsize
                 angles=self.__rolling(int(N_roll*roll_fac),max_deg)                                             # Get function for angles
                 pat_width=self.values.size[0]
                 pat_height=self.values.size[1]                                                    # Get image properties
                      
                 # Calculate maximum mismatch
                 x_mis=int(np.ceil(max(np.sin(angles*2*np.pi/360))*pat_height))
                 y_mis=int(np.ceil(max(np.sin(angles*2*np.pi/360))*pat_width))

                 # Get shape of template form
                 form_width=x_mis+pat_width
                 form_height=y_mis+pat_height
                                       
                 form=np.zeros([form_width,form_height])+1

                 # Put picture in form
                 form[int(np.floor(x_mis/2)):form_width-int(np.ceil(x_mis/2)),int(np.floor(y_mis/2)):form_height-int(np.ceil(y_mis/2))]=self.values.moire

                 # Loop
                 for i in range(0,int(N_roll*roll_fac)):
                     # Save load and save pattern
                     if(i==0):
                           # Get pattern
                           pattern=self.values.pattern
                           
                     # Don't save pattern again
                     else:
                           pattern=np.roll(pattern,roll_size) # Roll pattern to make different pictures visible maybe better save other varibale :)

                     # Rotated picture
                     rotated= rotate(pattern,angles[i] )
          
                     # Put rotated picture in form
                     rotated_width,rotated_heigth=np.shape(rotated)
                     x_diff=form_width-rotated_width
                     y_diff=form_height-rotated_heigth

                     output=np.zeros(np.shape(form))+1
                     output[int(np.floor(x_diff/2)):int(form_width-np.ceil(x_diff/2)),int(np.floor(y_diff/2)):int(form_height-np.ceil(y_diff/2))]=rotated
   
                     # add pattern to output
                     image=self.picture.one_to_zero(output)+form
                     image=self.picture.one_to_zero(image)
                     image = Image.fromarray(image*255)           
                     images.append(image)

                 # save as an animated gif
                 gif = images[0]
                 gif.save(fp="./Output/reality_check.gif", format='gif', save_all=True, append_images=images[1:],duration=duration,loop=loop)

                 # Verify that the number of frames in the gif equals the number of image files and durations
                 if(not(Image.open(gif_filepath).n_frames == len(images))):
                     window=ERROR(self.master,6)

                 print("Created GIF")

                 # OPEN GIF




      def __width_handler(self,N_s):
            '''Takes
                  N := Number of stribes
               Returns
                  s_wdth:= best estimaton of s_width for N stribes given a photo with size(nxm)
            '''
            x_size=self.values.size[1]                                  # !!! np.shape definition x,y,z=np.shape() x is the vertical and y the horizontal
            # calculate s_width
            ''' One cell contains N_s patern lik this:
            w1 ... ws_width | w1 .... ws_width | ...N_png times... |  w1 ... ws_width
            -> s_width=x_size/(N_s*self.values.N_png)
            '''
            s_width=int(round(x_size/(N_s*self.values.N_png)))     
            return s_width


      def __help(self):
            help_site=HELP(self.master,2)

      
      def __rolling(self,steps, max_angle=1):
                ''' Sinus model function for anglar mismatch
                        Takes:
                            steps   := Rolling steps
                            max_ang := Maximal mismatch angle
                        Returns:
                            angle   := Angular mismatch for each step
                '''

                # Linear
                x=np.linspace(0,1.5*np.pi,steps)
                angles=np.sin(x+1)*0.7*max_angle+0.3*max_angle
                return angles

      def __show_gif_again(self):
            self.__open_gif()
            


      def __open_gif(self,name=[]):
          imageViewerFromCommandLine = {'linux':'xdg-open',
                                        'win32':'explorer',
                                       'darwin':'open'}[sys.platform]
          if(name==[]):
                try:
                    subprocess.run([imageViewerFromCommandLine, self.values.output_loc+self.values.gif_name])
                except IOError:
                    window=WARNING(self.master,4)
          else:
                try:
                  subprocess.run([imageViewerFromCommandLine, self.values.output_loc+self.values.gif_name])
                except IOError:
                      window=WARNING(self.master,4)
                
      def __best_duration(self, N_steps=4,rep_time=0.5):
            duration=int((1000*rep_time)/N_steps)          # Calculate best duration and convert to ms
            return duration
      
      def __open_page3(self):
            ''' Function to go to page 2'''         
            self.master.destroy()
            root2= Tk()
            window2=GUI3(self.values,root2)

      def __finish(self):
            self.master.destroy()

################# HELP #################################### HELP ############################## HELP ########
            
class HELP(SIDESIDE):
        ''' Class for warnings'''
        def __init__(self, original,Nr):
              """Constructor"""
              SIDESIDE.__init__(self, original)
              self.Nr=Nr
              self.main.title("Help Nr. "+ str(self.Nr))#
              T = Text(self.main, height=10, width=45)
              T.place(x=20,y=20)
              ok=self.__warning_handler(T)
              backbtn = Button(self, text="Back", bg="red",width=8,font="Calibri 20",fg="white",relief="raised",command=lambda:self.__back()).place(x=120,y=220)

        def __back(self):           
              self.main.destroy()
              self.show()
              
        def __ok(self):
              self.decision=True
              self.main.destroy()
              self.show()

 
              
            
        def __warning_handler(self,T):
              if(self.Nr==0):
                    text="Use the slider to adjust the saturation level\n\n"+"Presh show to show the changes."
                    T.insert(END,text)
            
              if(self.Nr==1):
                    text="Use the slider to adjust the number of stips."+"\n"+"Note: With more strips you have a higher resolution, but to many may destroy the effekt!"
                    T.insert(END,text)

              if(self.Nr==2):
                    text="The reality simulation shows the worst case:\n"+"\n"+"The user does not move the pattern parallel, but with a changing angle!"
                    T.insert(END,text)
            


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
            
                    
              elif(self.Nr==1):
                    text="The best number for this illusion is between 2 and 7."
                    T.insert(END,text)


                                  
              elif(self.Nr==2):
                    text="Your picture is quite big!\n"+"This may cause problems\n"+"Recommended are max 3300 pixels"
                    T.insert(END,text)
                    return 0
                                  
              elif(self.Nr==3):
                    text="Your picture is quite small!\n"+"This may cause problems\n"+"Recommended are min 30 pixels"
                    T.insert(END,text)
                    return 0
                  
              elif(self.Nr==4):
                    text="Could not open GIF file.\n"+"Please do it by hand in the Oututfolder"
                    T.insert(END,text)
                    return 0
                  
              elif(self.Nr==5):
                    text="You have already set the values for all pictures.\n"+"Going back to the first again!"
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
              elif(self.Nr==1):
                    text="Don't leave blanck sides \n"
                    T.insert(END,text)
                    return 0


              elif(self.Nr==2):
                    text="Keine Dateien ausgewählt. \nBitte Dateien auswählen!"
                    T.insert(END,text)
                    return 0
              elif(self.Nr==3):
                    text="Pictures need to have the same size!"
                    T.insert(END,text)
                    return 0
              elif(self.Nr==4):
                    text="Bitte Titel des KT's angeben!"
                    T.insert(END,text)
                    return 0
              elif(self.Nr==5):
                    text="Wrong format, only png and jpeg are accepted"
                    T.insert(END,text)
                    return 0
               
              elif(self.Nr==6):
                    text="Something is wrong with the gif. \n"+"Numbers do not match!"
                    T.insert(END,text)
                    return 0
                   
              elif(self.Nr==7):
                    text="Something is wrong could not load files!"
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

          
      def create_stripes(self,size,N,s_width=2):
          # Create array    # Create array
          N_s=np.zeros([size[0],(N)*s_width])
          # Fill with ones
          N_s[:,0:s_width]=np.ones([size[0],s_width])

          # multiply
          pattern=np.tile(N_s,int(np.floor(size[1]/(N*s_width))))
          rest_array=np.zeros([size[0],size[1]%(N*s_width)])
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
                                                
#MAINGUI()
def main():
      # Initialize all values
      values=VALUES()
      
      # Open Tkinter window
      root=Tk()
      Window=GUI1(values,root)
      root.mainloop()
      print("Finished")

if __name__ == "__main__":
    main()
