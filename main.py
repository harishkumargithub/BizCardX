import easyocr as ocr
import skimage.color
from skimage import io
from skimage import filters
from PIL import Image
import streamlit as st
from streamlit_cropper import st_cropper as stc
import time


def alter_img(r):
    gray_img = skimage.color.rgb2gray(r)
    blur_img = skimage.filters.gaussian(gray_img)
    binary_img = blur_img < 0.8
    data = Image.fromarray(binary_img)
    data.save('data.jpg')


def text_extraction():
    extracted_data = []
    reader = ocr.Reader(['en'], gpu=True)
    result = reader.readtext('crop_img.jpg')
    for each in result:
        extracted_data.append(each[1])
    return extracted_data


def img_crop(k):
    new_img = Image.open('data.jpg')
    crop_img = stc(img_file=new_img, realtime_update=False, box_color='blue', key=k)
    _ = crop_img.thumbnail((200, 200))
    st.image(crop_img)
    save = st.button(label='Confirm the cropped image !?', key=k+10)
    if save:
        Image.Image.save(crop_img, fp='crop_img.jpg')
        temp = text_extraction()
        return temp


def extract_crop():
    data_in_need = {'Company_Name': '', 'Card_holder_name': '', 'Designation': '', 'Email': '', 'URL': '','Phone_number': '','Address': ''}
    key = 1
    for each in data_in_need:
        st.header('Crop the image to take '+each+ ' as the input, double tap on image to confirm crop render')
        data = img_crop(key)
        if data:
            data_in_need[each] = data
            key += 1
            data = None
            st.write(data_in_need)
        else:
            time.sleep(25)
            st.write('Timer expired')
            break
    return data_in_need


with st.container():
    st.header('Welcome to my BizCardX Project 👍')
    raw_img = st.sidebar.file_uploader(label='Upload images here')
    if raw_img:
        img = io.imread(raw_img)
        st.sidebar.image(img)
        st.write('The image will be converted to black and white format to enhance search results')
        alter_img(img)
        processed_data = extract_crop()
