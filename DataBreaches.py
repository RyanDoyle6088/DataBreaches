"""
    The goal of this project is to use lists, dictionaries, data structures, functions, iterations,
    and data analysis to analyze and display information about the biggest data breaches in history.
    These breaches give availability of sensitive information to whoever can get it. This project
    focuses on some of the biggest data breaches in the past. We will use the open file function,
    build a dictionary of strings and ints from the excel data, pass the dictionary into a list to be
    sorted into 10 tuples, then sort them for whatever piece of data we want.
"""
import csv
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np

def open_file(message):
    
    '''
        This is the starting function for this project. The function will
        open a file that is inputted from the user and return a file pointer. 
        In this project, we have set the specific breach data file to be equal
        to an empty string, to save time for the user so they don't have to enter
        the name every single time they want to run the code.
    '''
    
    FileFound=False

    filename=input(message)
    #Message is passed through as the input
    if filename=='':
        filename='breachdata.csv'
        #If the user just presses enter, an empty string, it passes thru the breachdata.csv file
  
    while (FileFound==False):
            
        try:
           fp = open(filename, encoding='utf8')
           return fp
       #try-except for the filenotfound error incase the file does not exist
       #encoding to read the csv file
        except FileNotFoundError:
            #If filenotfound, print the error message and reprompt
           print('[ - ] File not found. Try again.')
           filename = input("[ ? ] Enter the file name: ")
    
    
def build_dict(reader):
    '''
        This function accepts a CSV reader as input and returns the required 
        dictionary. It iterates over the CSV reader and with each iteration, 
        extracts the needed data and remove any extra whitespaces. We will then
        build a master dictionary using the indexes of the strigs and ints
        for our values in the csv breach file. We will then return this dictionary
        of lists and tuples.
    '''
    entity_string_year_int_dict={}
    master_dict={}
    #Creating our 2 empty dictionaries
    
    next(reader, None)
    #Skip header
    for line in reader:
        
        news_sources_list=[]
        #creating our empty list
        valid_record=True

        entity=line[0]
        story=line[4]
        sector=line[5]
        method=line[6]
        records_lost=line[2]
        #Indexes for our values in csv file
        records_lost=records_lost.replace(',','')
        #need to get rid of commas

        if records_lost=='':
           records_lost=0
           #If no records lost value we set it equal to 0
           
        year=line[3]
        news_sources=line[11]

        if (entity=='') or (story=='') or (sector=='') or (method=='') or (year=='') or(news_sources==''):
           valid_record=False

        news_sources_list=news_sources.split(',')

        try:
            records_lost=int(records_lost)
            #try except for trying to make ints of the records and years since theyre num values
            
            year=int(year) 
        except ValueError:
            #We know they will be ints
            
            continue
        if valid_record==True:
            
           entity_string_dict={}
           year_string_dict={}
           #dicts for our string values
           main_tuple=()
           tuple_list=[]
           #the list of tuples
           
           tuple1=(records_lost,year,story,news_sources_list)
           #tuple of records lost, stories, list of sources
           tuple2=(sector,method)
           #tuple of sector and method value
           entity_string_dict[entity]=tuple1
           year_string_dict[year]=tuple2
           #dictionary equal to tuple value for year
           main_tuple=(entity_string_dict,year_string_dict)
           tuple_list.append(main_tuple)
                    
           if entity in master_dict:
                           
              list_value=master_dict.get(entity)
              list_value.append(tuple_list[0])
              master_dict[entity]=list_value
              #list value is the entity value of our master dictionary
            
           else:
               
               master_dict[entity]=tuple_list

    return master_dict
    #We return the value we want in the form of our newly built dict

def top_rec_lost_by_entity(dictionary):
    '''
        This function will accept the breach dictionary as created by the build dict 
        function above and returns a sorted list in descending order of records lost 
        of the top 10 entities that lost the most records. To break ties, the returned 
        list should be sorted by entity alphabetically. The returned list will contain 
        10 tuples, each tuple containing the entity name and total records lost by that entity.
        We will return the sorted list of the top records lost.
    '''
    #counting records lost by entity
    

    sorted_breach_dict_list=[]
    #List that we will append to
    for key in dictionary:
        
        tuple_lost_records=()
        #tuple for lost records
        list_key=dictionary[key]
        #Key in master dictionary
       
              
        total_records_lost=0
        for value in list_key:
            
            list_value=value[0].get(key)
            #entity at index 0
            total_records_lost=total_records_lost+int(list_value[0])
            #making the total records lost
           
        tuple_lost_records=(key,total_records_lost)
        sorted_breach_dict_list.append(tuple_lost_records)
        #appending the tuple of lost records to the list we sort in next step 


    sorted_breach_dict_list.sort(key =itemgetter(1,0),reverse=True)
    #descending order sorted by entity index, and alphabetically
    return sorted_breach_dict_list[:10]
    #now we return it just up to 10
    

def records_lost_by_year(dictionary):
    '''
       This function accepts the master dictionary and produces a sorted list
        of total records lost within each year. This is similar to the previous 
        function, except that instead of counting records lost by entities, we
        are counting records lost by year. Also, instead of returning only the 
        top 10, this function should return all records by year. The list  
        contains tuples such that each tuple contains the year and the corresponding 
        total records lost in that year, which is why we create tuple of lost records.
    '''
    #counting records lost by year
    
    
    records_lost_dict={}
    records_lost_by_year=[]
    #creating our empty dict and list
  
    for key in dictionary:
        
        tuple_lost_records=()
        list_key=dictionary[key]
       
        total_records_lost=0
        for value in list_key:
           
            list_value=value[0].get(key)
            #key at index 0 for our records lost
            year=list_value[1]
            records_lost=int(list_value[0])
            #list index 0, int value
          
            if year in records_lost_dict:
                
               exist_records_lost_value=records_lost_dict.get(year)
               #year for the records lost 
               total=int(records_lost)+int(exist_records_lost_value)
               #existing records lost and the records lost in year in dict
               records_lost_dict[year]=total
              
            else:
                
               records_lost_dict[year]=records_lost

    for key in records_lost_dict:
        
        records_lost=records_lost_dict[key]
        tuple_records_lost=(key,records_lost)
        #creating the tuple with the year and records lost for that year
        records_lost_by_year.append(tuple_records_lost)
        #appending it to the list we return
        

    records_lost_by_year.sort(key=itemgetter(1,0),reverse=True)
    return records_lost_by_year    
    #sorted in descending order

def top_methods_by_sector(dictionary):
    '''
        This function takes in the breach master dictionary and returns a dictionary 
        of dictionaries. The returned dictionary contains keys for all sectors 
        found in the breach dictionary. The values ofthis dictionary are dictionaries
        that contain the method as key and the corresponding count as value.
    '''
    
    records_by_sector={}
    records_lost_by_year=[]
    
    for key in dictionary:
        
        tuple_sector_records=()
        list_key=dictionary[key]
       
        for value in list_key:
            #key of our dictionary, values, we want 1 and 0
           
            for value_1 in value[1]:
                
                sector=value[1][value_1]
                
                if sector[0] in records_by_sector:
                    #if sector is in our dict, it is a current sector                   
                   current_sector=records_by_sector[sector[0]]
                
                   if sector[1] in current_sector:
                       #if sector is in the current records by sector
                                            
                       total=current_sector[sector[1]]
                       total=total+1
                       #adds our total of strings for displaying the data
                       current_sector[sector[1]]=total
                       records_by_sector[sector[0]]=current_sector
                        
                   else:
                       
                       current_sector=records_by_sector[sector[0]]
                       current_sector[sector[1]]=1
                       records_by_sector[sector[0]]=current_sector
                       #current sector
                                           
                else:
                    
                   records_by_sector[sector[0]]={}
                   sector_type={}
                   sector_type[sector[1]]=1
                   records_by_sector[sector[0]]=sector_type
                         
    return records_by_sector
    #return the records by sector for each specific case

        
def top_rec_lost_plot(names,records):
    ''' Plots a bargraph pertaining to
        the cybersecurity breaches data '''
        
    y_pos = np.arange(len(names))

    plt.bar(y_pos, records, align='center', alpha=0.5,
            color='blue',edgecolor='black')
    plt.xticks(y_pos, names, rotation=90)
    plt.ylabel('#Records lost')
    plt.title('Cybersecurity Breaches',fontsize=20)
    plt.show()
    
def top_methods_by_sector_plot(methods_list):
    ''' Plots the top methods used to compromise
        the security of a sector '''
    methods = [] ; quantities = []
    for tup in methods_list:
        methods.append(tup[0])
        quantities.append(tup[1])
    labels = methods
    sizes = quantities
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

    plt.pie(sizes, labels=labels, colors = colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    plt.show()
    
def main():
    '''Our main function will print the menu as an input, the user can see the options
    laid out for them, then they must input a choice, between 1 and 5. If the choice is not
    valid, we reprompt. For each choice, the user must input a file. It defaults to breachdata,
    but can also accept breach data small and medium if needed. Choice one displays the
    data for most records lost by internet entities, such as AOL. Choice 2 displays the
    most records lost for each year. Choice 3 will show the top methods used for each
    sector. Choice 4 will search stories about the incident from our data. Choice 5 is 
    the exit command, so the code will print the goodbye message and break.'''
    BANNER = '''
    
                 _,.-------.,_
             ,;~'             '~;, 
           ,;                     ;,
          ;                         ;
         ,'                         ',
        ,;                           ;,
        ; ;      .           .      ; ;
        | ;   ______       ______   ; | 
        |  `/~"     ~" . "~     "~\'  |
        |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
         |   |        }:{        |   | 
         |   l       / | \       !   |
         .~  (__,.--" .^. "--.,__)  ~. 
         |     ---;' / | \ `;---     |  
          \__.       \/^\/       .__/  
           V| \                 / |V  
            | |T~\___!___!___/~T| |  
            | |`IIII_I_I_I_IIII'| |  
            |  \,III I I I III,/  |  
             \   `~~~~~~~~~~'    /
               \   .       .   /
                 \.    ^    ./   
                   ^~~~^~~~^ 
                   
           
           ~~Cybersecurity Breaches~~        
                   @amirootyet    
                
    '''
    
    print(BANNER)
    
    MENU = '''  
[ 1 ] Most records lost by entities
[ 2 ] Records lost by year
[ 3 ] Top methods per sector
[ 4 ] Search stories
[ 5 ] Exit

[ ? ] Choice: '''
    
    choice=input(MENU)
    while choice not in ('1','2','3','4','5'):
        #if choice isnt 1-5, we print error message and reprompt
        print('[ - ] Incorrect input. Try again.')
        choice=input(MENU)

    if choice!='5':
        #if choice is not 5, we run the open file function to return fp
        fp=open_file("[ ? ] Enter the file name: ")
        reader=csv.reader(fp)
        master_dictionary=build_dict(reader)
                         
    while choice!='5':
 
       if choice=='1':
           #if choice is 1, we will return lists of records
          names=[]
          records=[]
          
          print("[ + ] Most records lost by entities...")
          rec_lost_by_entity_list=top_rec_lost_by_entity(master_dictionary)
          #we use the master dictionary from our build dict funtion
          #finding the top records lost by the entity
          counter=1
          for value in rec_lost_by_entity_list:
              print("-"*45)
              #formatting
              print("[ {:2d} ] | {:15.10s} | {:10d}".format(counter,value[0],value[1]))
              names.append(value[0])
              #appending the names of entity to our list to siplay at index 0
              records.append(value[1])
              #appending the numbers of records to the index 1
              counter=counter+1


          plot_graph=input('[ ? ] Plot (y/n)? ').lower()
          #ask if they want plot
          if plot_graph=='y':
              top_rec_lost_plot(names, records) 
              #if they want to plot, pass the lists through the records lost plotting tool
              
              
       if choice=='2':
           
          years=[]
          records=[]
          print("[ + ] Most records lost in a year...")
          records_lost_by_year_list=records_lost_by_year(master_dictionary)
          counter=1
          for value in records_lost_by_year_list:
              print("-"*45)
              print("[ {:2d} ] | {:2d}          | {:10d}".format(counter,value[0],value[1]))
              years.append(value[0])
              #using years this time instead of names
              records.append(value[1])
              #we still use the records value at index 1
              counter=counter+1


          plot_graph=input('[ ? ] Plot (y/n)? ').lower()
          #ask if they want plot
          if plot_graph=='y':
              
              top_rec_lost_plot(years, records) 
              #this time we pass the years and the records into the plot tool
            


       if choice=='3':
           
          print("[ + ] Loaded sector data.")
          #sectors this time
          
          records_by_sector=top_methods_by_sector(master_dictionary)
          #using the dictionary for the records by sector rather than entity
          list_sectors=[]
          #list for our sectors
          
          for key in records_by_sector:
              #key in dict for sector
              
              list_sectors.append(key)
              #we append it to our list of sectors

          list_sectors.sort()
          sector_string=''
          for value in list_sectors:
              
              sector_string=sector_string+value+' '
              #adding the value to the string from our list

          print(sector_string)
          sector_choice=input("[ ? ] Sector (case sensitive)? ")
          #the user must input the sector they want to see the data for, 15 options
          print("[ + ] Top methods in sector {}".format(sector_choice))
          #print the data and display what sector its for

          methods_dict=records_by_sector[sector_choice]
          #user choice of sector, in our records of sector
          counter=1
          for i in sorted (methods_dict.keys()):
              #in our dict
              
              print("-"*45)
              print("[ {:2d} ] | {:15.10s} | {:10d}".format(counter,i,methods_dict[i]))
              #formatting, we want to return counter for the amount, then the method of breach
              
              counter=counter+1

          plot_graph=input('[ ? ] Plot (y/n)? ').lower()
          if plot_graph=='y':
              methods_list=sorted(methods_dict.items(),key=itemgetter(1), reverse=True)
              #if they want to plot, we sort at index 1, descending order, for
              #a list of our items, then pass through the top methods by sector plot tool
              top_methods_by_sector_plot(methods_list)

                   
       if choice=='4':
           
          entity_name=input("[ ? ] Name of the entity (case sensitive)? ")
          #user input for name of entity

          while (entity_name not in master_dictionary):
              #if they don't use a valid entity
              
             print("[ - ] Entity not found. Try again.")
             #need to enter a valid entity
             entity_name=input("[ ? ] Name of the entity (case sensitive)? ")
             
             
          entity_list=master_dictionary[entity_name]
          #making our list from master dict, for the entity name this time
          print("[ + ] Found"+" "+str(len(entity_list))+" " + "stories:")
          #we print for how many stories found for entity entered
          
          counter=1
          for value in entity_list:
              
              list_values=value[0]
              print("[ + ] Story {}: {:10s}".format(str(counter),list_values[entity_name][2]))
              #We then print the actual story, and which number story it is in the sequence
              counter=counter+1
                   
       choice=input(MENU)
       #outside of loop, so if plot=n it will reprompt here for choice
       while choice not in ('1','2','3','4','5'):
           #reprompt for choice not in options
           
          print('[ - ] Incorrect input. Try again.')
          choice=input(MENU)

    print("[ + ] Done. Exiting now...")

if __name__ == "__main__":
     main()