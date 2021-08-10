# OnlineKart Commerce Website

An E-commerce website built using Django.<br>
Deployed URL: https://onlinekart.pythonanywhere.com/

## Key Features 
* Send email verification link to users when they Sign Up or Reset Password
* User Authentication (Login/Logout)
* Product Store, Product Details
* Review and Rating System
* Dashboard, My Orders, Edit Profile, Change Password 
* Product Gallery, Product Variations
* Payment Integration (Paypal)
* Security Measures Implemented (Admin Honeypot,.env file)

Note:- To make payment after placing order in website, refer to the screenshot below that contains credit card number with expiry date and CVV.

## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. <br><br>
To activate environment, 

1. Command on mac/linux:

```
source env/bin/active
```

2.  Command on Windows:

```
env\Scripts\Activate
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Screenshots of Website
![1](https://user-images.githubusercontent.com/67990422/128908476-ee0adee1-401a-4920-a705-37b74540dc07.PNG)
![10](https://user-images.githubusercontent.com/67990422/128908718-3aae8d43-d253-438d-827a-1eedc75cff94.PNG)
![2](https://user-images.githubusercontent.com/67990422/128908341-7b99da45-9ed6-4287-9ffd-449e714fba15.PNG)
![3](https://user-images.githubusercontent.com/67990422/128908609-a6f35d23-0fd4-4582-b1ef-9b71ffc10746.PNG)
![4](https://user-images.githubusercontent.com/67990422/128908645-c4cb5839-ff62-495c-acb4-ea3468229e16.PNG)
![5](https://user-images.githubusercontent.com/67990422/128908425-cde88546-142e-4bd2-9d65-f129a58f3202.PNG)
![6](https://user-images.githubusercontent.com/67990422/128908445-e15b5f46-bc75-4457-913c-256fa84b7c99.PNG)
![7](https://user-images.githubusercontent.com/67990422/128908666-669fff46-1a6f-4985-9430-a09ad26e8858.PNG)
![8](https://user-images.githubusercontent.com/67990422/128908687-9c792958-c4c1-4dde-b50a-036c5b35bcc9.PNG)
![9](https://user-images.githubusercontent.com/67990422/128908707-d8af32d6-ae70-4ec6-9ace-984ff3c401bf.PNG)

