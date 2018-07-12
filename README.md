# URL Analysis Tool

This Python project is used to analyse a great number of urls. It achieves the following functions:
- Detect the status code of the url.
- Detect the Content Management System (CMS) of the url. 
Mainly focus on Opencart, Prestashop, Wordpress, Magento, Shopify and Squarespace.
- Classify the url according to the website content.
- Detect whether a user can advertise in the website (Wordpress only).

The CMS Detection results come from website "https://whatcms.org/", and the Classification results come from https://fortiguard.com/webfilter/. To speed up the detection, a multiple processors method is used.

The input is a .txt file, and each line has a website domanin name, like: "https://www.shore-lines.co.uk/".

The outputs are two .csv file, "target.csv" and "problem.csv". They are used to record the result of the analysis and the error website respectively.

## Prerequisites
- Python3.+
- Chrome browser
- chromedriver (http://chromedriver.chromium.org/)
- MPI

Please install the requirements.txt file using the command below:
```
pip install -r /path/to/requirements.txt
```

## How to use
```
mpiexec -n number_of_process python3 Main.py -f your_input_file
```
-n is the number of processors you want to use<br>
-f is the file you want to process.<br>

For linux user, if you want to shut down your computer after finishing all the dection, you can use the code in line 52 and 53 in Main.py script. And adding --allow-run-as-root in the command. like:
```
mpiexec --allow-run-as-root -n 20 python3 Main.py -f input.txt
```
## Authors

* **[Hongyi Lin](https://github.com/Hongyil1)** 

## License

This project is licensed under the MIT License

## Demo
<img width="544" alt="image 1" src="https://user-images.githubusercontent.com/22671087/42612132-e32118aa-85dc-11e8-8c68-e9798ad915f6.PNG">

## Sample Result
<img width="676" alt="image 2" src="https://user-images.githubusercontent.com/22671087/42612987-c5a4e928-85e1-11e8-9d37-2af075f7f767.PNG">
