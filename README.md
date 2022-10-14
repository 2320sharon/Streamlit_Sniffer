# Streamlit Sniffer 👑🐕
- A Python Streamlit app for sorting through imagery. Check it out [on Streamlit](https://share.streamlit.io/2320sharon/streamlit_sniffer/sniffer.py)
</br>

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/2320sharon/streamlit_sniffer/sniffer.py)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blueviolet.svg)](https://www.python.org/downloads/release/python-310/)

### Rate your Images with Sniffer
- Use a customizeable slider to rate your images
</br>
<img src="https://user-images.githubusercontent.com/61564689/195918016-e39ef258-b694-4fbb-9dc3-1a93279fcdd5.gif" width=550, height = 500>
</br>

### Rate your Images with Sniffer with Yes/No Buttons
</br>
<img src="https://user-images.githubusercontent.com/61564689/168155940-8f3a0408-48a2-4998-894e-3d2d861847de.gif" width=650 >
</br>

## How to Install Sniffer on Your Computer 🐕 :computer:
1. Open your terminal<a href="url"><img src="https://user-images.githubusercontent.com/61564689/168151976-84c1ed67-518b-40b5-845e-6d859e43595b.png" align="center" height="30" width="30" ></a>
2. Create an environment with Streamlit installed. See [Streamlit's instructions](https://docs.streamlit.io/library/get-started/installation#:~:text=Set%20up%20your%20virtual%20environment) for more details for your compouter.
3. Inside your virtual environment with streamlit install run either `pip install pillow` or if you're using an Anaconda conda environment use `conda install -c conda-forge pillow`.
4. You're done! 🎊

## How to Use Sniffer on Your Computer 🐕 🔧
1. Create an environment with Streamlit installed. See [Streamlit's instructions](https://docs.streamlit.io/library/get-started/installation#:~:text=Set%20up%20your%20virtual%20environment) for more details for your compouter.
2. Open your terminal<a href="url"><img src="https://user-images.githubusercontent.com/61564689/168151976-84c1ed67-518b-40b5-845e-6d859e43595b.png" align="center" height="30" width="30" ></a>

 3. Go to the directory where you installed Sniffer
   `cd <location where you saved Sniffer>`
4. Run `streamlit run sniffer.py`
5. Wait for it to open your browser and you're done! 🎊


## ✨ New Feature ✨ Resize Image Sliders
</br>
<img src="https://user-images.githubusercontent.com/61564689/195921120-3837906b-44be-4e5e-ab61-4179f3a0d23c.gif" width=465 >
</br>
1. Check the Show Resize Controls checkbox to show the height and width sliders
2. Use the height and width sliders to choose height and width of your image
3. Check the Resize checkbox to resize your image instantly ⚡
4. Uncheck the Resize checkbox to restore your image to its original size

## ✨ New Feature ✨ New Slider to Numerically Rate Images

<img src="https://user-images.githubusercontent.com/61564689/195921252-e06ea4da-a51d-4651-887d-041062d37bbf.jpg" width=450 height=400>
<img src="https://user-images.githubusercontent.com/61564689/195922494-df9f1c62-4026-41fe-8b9f-bb9fd61e6d45.png" width=450 height=180>

1. Under Choose Controls click the radio button that says `scale`
2. Change the minimum and maximum of the slider range by using the controls under `change slider range`
3. Use the slider to rate your image
4. Check `Next` to rate your image and save your rating to the csv file.


## ✨ Features ✨ Black Pixel Feature
</br>
<img src="https://user-images.githubusercontent.com/61564689/171754117-9c695747-1221-49d2-89e1-57498f36836a.gif" width=475 >
</br>
1. Turn on the black pixel filter to filter out images with black pixels in your dataset </br>
2. You can use the checkbox to see images that exceed the black pixel limit you set </br>
3. The images that exceed the black pixel limit will not be shown (except the first one) </br>

## Don't want to use Streamlit
- Check out the orignal version of [Sniffer 🐕](https://github.com/2320sharon/Sniffer) that you can download on you local computer 

## Tips for Customization 🎨
1. Check out the offical [Streamlit Docs](https://docs.streamlit.io/) for adding cool components like dropdown menus and more!

## How to Install Streamlit
[Check out Streamlit's Instructions](https://docs.streamlit.io/library/get-started/installation)

## Disclaimers ⚠️
1. This version outputs all images as `.jpg`.
