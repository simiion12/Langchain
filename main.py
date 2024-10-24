import streamlit as st
from chatbot import ChatBot
import time


def main():
    st.title("Interactive Chatbot with Web Search")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chatbot = ChatBot()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Process input and get response
            response = st.session_state.chatbot.process_input(prompt)

            # Simulate streaming by displaying response chunk by chunk
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)  # Add a small delay between chunks
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()