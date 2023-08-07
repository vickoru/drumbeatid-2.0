from typing import final
import streamlit as st
import requests
from wavinfo import WavInfoReader
from scipy.io import wavfile
from scipy.io.wavfile import read
#from dotenv import load_dotenv
#from pydub import AudioSegment



# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
url = "http://localhost:8000"
# url_predict = "http://localhost:8000/predict"
#load_dotenv()
#url = os.getenv('API_URL')

# Set page tab display
st.set_page_config(
   page_title="Drumbeat ID Project 🥁",
   page_icon= 'X',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Main Text on Homepage
'''
# User Interface for Drum Beat ID 🥁

### Upload WAV-File and get the result of our classification:
'''
# File uploading section
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_wav = st.file_uploader("Choose a WAV file", type="wav", accept_multiple_files=False)



if uploaded_wav is not None:
    # read and play the audio file
    st.write('### Play audio')
    audio_bytes = uploaded_wav.read()
    st.audio(audio_bytes, format='audio/wav')

    if st.button('Analyze Audiofile'):
        # Progress bar
        st.spinner("Sending the Audiofile to the API ...")
        # calling API for prediction
        res = requests.post(url + "/upload_wav", files={'wav': audio_bytes})
        genre = res.json()['genre']
        st.write('### Analysis of Wave-File performed ! 🎉')
        # res = requests.post(url + "/upload_wav", files={'wav': uploaded_wav })
        # genre = res.json()['genre']
        # # genre = "Rock"

        with st.expander("See result of analysis 👀"):
            if len(genre) > 1:
                st.write(
                    f"### Not so sure about the style of your drumbeat 😨 🤖")
                st.write(
                    f'### It could be _{genre[0]}_ or _{genre[1]}_'
                )
                st.image("https://i.pinimg.com/originals/45/76/ba/4576ba99b4c56ad17c8a3bd40e1e5b84.jpg", width=300)
                st.caption(f'### Clyde Stubblefield, collaborated with James Brown, 1943-2017', unsafe_allow_html=False)
            else:
                genre = genre[0]
                st.write(f"### The style of your drumbeat is:")
                st.write(f"## _{genre.capitalize()}_")
                if genre == "rock":
                    st.image("https://www.rollingstone.de/wp-content/uploads/2016/04/01/12/John-Bonham-GettyImages-77186814-992x560.jpg", width=500)
                    st.caption(f'### John Bonham, drummer of Led Zeppelin, 1948-1980', unsafe_allow_html=False)
                elif genre == "jazz":
                    st.image("https://www.bluenote.com/files/2019/03/TonyWilliams_byFrancisWolff.jpg", width = 500)
                    st.caption(f'### Tony Williams, 1945-1997', unsafe_allow_html=False)
                elif genre == "funk":
                    st.image("https://drummagazine.com/wp-content/uploads/2018/11/James-Diamond-WIlliams-Ohio-Players_2.jpg", width = 500)
                    st.caption(f'### James Diamond, drummer of Ohio Players, 1950-today', unsafe_allow_html=False)
                elif genre == "latin":
                    st.image("https://npr.brightspotcdn.com/dims4/default/f128c94/2147483647/strip/true/crop/800x533+0+0/resize/880x586!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F6b%2Ff5%2Fb8d62d964faa80d7f334a0500285%2Ftito-puente-at-timbales.jpg", width=500)
                    st.caption(f'### Tito Puente, 1923-2000', unsafe_allow_html=False)
                elif genre == "hiphop":
                    st.image("https://drummagazine.com/wp-content/uploads/2021/12/questlove-soundclash-scaled.jpg", width=300)
                    st.caption(f'### Questlove, drummer of The Roots, 1971-today', unsafe_allow_html=False)
                else:
                    st.image("https://i.pinimg.com/originals/45/76/ba/4576ba99b4c56ad17c8a3bd40e1e5b84.jpg", width=300)
                    st.caption(f'### Clyde Stubblefield, collaborated with James Brown, 1943-2017', unsafe_allow_html=False)

            # st.balloons()

#OLD CODE

# If Button 'Analyze Audiofile' is pushed following code will be sent to API
#if uploaded_wav is not None and st.button('Analyze Audiofile'):
    #st.spinner("Sending the Audiofile to the API ...")
   # res = requests.post(url + "/upload_wav", files={'wav': uploaded_wav })
    #genre = res.json()['genre']

   # if res.status_code == 200:
       # print('OK')
       # st.write(genre)

        # y, sr = librosa.load(uploaded_wav, duration=6)
        # print(sr)
        # # parameters = {
        #     'waveform': y,
        #     'sampling_rate': sr
        # }

        # prediction = requests.get(url_predict, params=parameters).json()['genre']
        # st.write(prediction)
        # '''
        # ## Analysis of Wave-File performed ! 🎉
        # ### Result: This song is definetely a Helene Fischer-Schlager
        # '''
        # # st.balloons()

   # if res.status_code != 200:
      #  '''
      #  Analysis was not successful. Please try again...
      #  print(res.status_code, res.content)
      #  '''
