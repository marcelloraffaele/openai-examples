import streamlit as st
import datetime

def increment_counter(val):
    st.session_state.count += val
    st.session_state.last_updated = datetime.datetime.now().time()

def reset_counter():
    st.session_state.count = 0
    st.session_state.last_updated = datetime.datetime.now().time()

st.title('Counter Example')

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

increment_value = st.number_input('Increment value', value=1, step=1)

st.button('Increment', on_click=increment_counter, args=(increment_value,))
st.button('Reset', on_click=reset_counter)

st.write('Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)
