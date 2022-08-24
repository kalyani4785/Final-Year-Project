# Final-Year-Project
Final Year Project (Automated sales & inventory management system).

## ✔ Get Up & Running in 5 minutes (For Windows OS):

*📜 Note:- A stable internet connection is required while executing the steps given below.*

1) Download code .zip file & extract to a folder.

2) Open the extracted project in file explorer and goto the following folder location:

	`root project folder -> sales_n_inventory_web -> _init_sdk`
	<br>*(In this location, .json file will be found.)*

3) Copy the full-qualified location of .json file.
 
4) Now goto the following folder location:

	`root project folder -> sales_n_inventory_web -> sales_app`
	<br>*(In this location, a file named "views.py" will be found.)*
	
5) Open "views.py" with any text editor & goto line-number 26 and replace the default location with the new copied location of .json file.

	*For Example: 
	
	*(Line-Number 26 in views.py)*
		<br>`cred = credentials.Certificate('paste/your/new/copied/location/of/.json/file/here')`
		
	*📜 Note:- Use forward slash (/) inside location path.*
	

6) Goto root project folder which contains the file named as "requirements.txt".

7) Goto to windows explorer address bar -> type "cmd" & press enter key.

8) Now create a virtual environment to run the app by running these commands in CMD in the given sequence:
	
	-> `python -m venv my-venv`

	-> `my-venv\Scripts\activate.bat`

	-> `pip install -r requirements.txt`
	
	*📜 Note:- After executing "pip install" command, it will take some time to download the project dependencies from the internet.*

9) After installing dependencies, don't close the cmd window. Now run these commands.

	-> `cd sales_n_inventory_web`

	-> `python manage.py runserver`
  


