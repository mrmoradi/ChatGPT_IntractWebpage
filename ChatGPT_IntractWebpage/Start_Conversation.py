from ChatGPT_IntractWebpage_Class import ChatGPTClass
import easygui
import pyperclip



#---------------------------------
file_address = easygui.fileopenbox()
#---------------------------------

chatGPTClass = ChatGPTClass()


# file_address = f"E:/CMU Project/AI/PPI/drew.pdf"
# question = "list all the protein-protein interactions (PPIs) within HeLa cells described in the paper."


# file_address= 'E:/CMU Project/AI/PPI/Dual.pdf'
# question='List all the protein-protein interactions (PPIs) described in the paper? described in the paper.'


# file_address = f"E:/CMU Project/AI/PPI/fchem-09-811190.pdf"
# question='List all the protein-protein interactions (PPIs) described in the paper? described in the paper.'


# file_address = f"E:/CMU Project/AI/PPI/ijms-24-01282.pdf"
# question='List all the protein-protein interactions (PPIs) described in the paper? described in the paper.'



# file_address = f"E:/CMU Project/AI/PPI/96643-v1.pdf"
question='List all the protein-protein interactions (PPIs) described in the paper? described in the paper.'




Answer_percentage = "10%"


file_address_Backup = file_address
# it means first tab is user and the second one is chatgpt
user_asking = True

user_respons = ""


# gpt_respons = f"""

# Imagine you are a supervisor, and you must ask this question based on the contents of an attached file from another AI. Your goal is to read and analyze the othe AI's aswer to your question, ensuring the aswer completly generated by the other AI and not by you.

# **Instructions for Asking a Question to Another AI:**

# **Steps to Follow:**

#    Describe the type of file you are attaching.
  
#    In the following lines, ask your question "{question}".
  
#    Your goal is to obtain at least {Answer_percentage}% of your answer from another AI. Formulate your question in a way that leverages the AI's capabilities to provide the information you need.
  
#    Remember, the attached file is for your reference and supervision purposes only. Do not use the information in the file directly in your question, or anwering the question by your self, it means the other AI has to answer to the question.
  
#    Proceed to ask your question to the other AI. Your message will be sent to the other AI, and its responses will be sent back to you. Do not provide explanations or additional context about your actions.
  
#    The response must be written specifically for you. It should not involve saving a file or any similar action.
  
#    You are interacting with an AI identical to yourself, so use this understanding to get the most accurate and comprehensive answer.
  
#     Aim to get your answer in less than 10 interactions. If you can obtain an answer that meets over {Answer_percentage}% of your expectations, proceed with "Finish."

# **Important Note:** Do not tell me anything, explain your actions, or describe your intentions. Just analyze the responses from the other AI and work independently to achieve your goal.


# """






gpt_respons = f"""



   write only 1 line about the type of file is attaching, for example 'This is a PFD file.'.
  
   In the following lines, write this question: "{question}".
  
"""

print(file_address)

pyperclip.copy(gpt_respons)

while not ("Finish" in user_respons and user_respons.splitlines() and "Finish" in user_respons.splitlines()[-1]):


    if user_asking:

        # temp_msg = f"""


        #                - Guide the other AI to provide answers to your question ("{question}"). Try and try and try... untile you get your answers 
                                              
        #                 - Do not explain anything to me. Focus solely on guiding the other AI to get your answers, aiming to meet over {Answer_percentage}% of your expectations.

        #                 - In each response, you must check and analyze to verify the answer. If it satisfies your requirements, simply write "Finish."
                        
        #                 - Remember, it is crucial that the other AI finds your answer. You must act like a supervisor, guiding, but everything must be done by the other AI, not manually by you. Do not suggest any manual tasks to the other AI.
                        
        #                 - Try to get your answer in less than 10 interactions. If the answer meets over {Answer_percentage}% of your expectations, write "Finish." Avoid asking the same question repeatedly.
                        
        #                 - Do not explain anything or explain what you are doing. Just analyze the other AI's answer and work independently. 
                        
        #                 - If the other AI answers your question satisfactorily, write "Finish."
                        
        #                 - If the other AI needs to reupload the file, write only "Reuploading..."
                
        #         Below is its answer to your previous request:

        #     """
        temp_msg = f"""

                        -Imagine you are a supervisor, and you must analyze answer based on the contents of an attached file from another AI. Your goal is to read and analyze the othe AI's aswer to your question, ensuring the aswer completly generated by the other AI and not by you.

                        - **Important Note:** Do not tell me anything, explain your actions, or describe your intentions. Just analyze the responses from the other AI and work independently to achieve your goal.

                       - Guide the other AI to provide answers to your question ("{question}"). Try and try and try... untile you get your answers 
                                              
                        - Do not explain anything to me. Focus solely on guiding the other AI to get your answers, aiming to meet over {Answer_percentage}% of your expectations.

                        - In each response, you must check and analyze to verify the answer. If it satisfies your requirements, simply write "Finish."
                        
                        - Remember, it is crucial that the other AI finds your answer. You must act like a supervisor, guiding, but everything must be done by the other AI, not manually by you. Do not suggest any manual tasks to the other AI.
                        
                        - Try to get your answer in less than 10 interactions. If the answer meets over {Answer_percentage}% of your expectations, write "Finish." Avoid asking the same question repeatedly.
                        
                        - Do not explain anything or explain what you are doing. Just analyze the other AI's answer and work independently. 
                        
                        - If the other AI answers your question satisfactorily, write "Finish."
                        
                
                Below is its answer to your previous request:
                [
                {
                    pyperclip.paste()
                }
                ]
            """

        aa = pyperclip.paste()

        if user_respons != "":
            #temp_msg = temp_msg + aa
            pyperclip.copy(temp_msg)

        print("User:_________________________________________________________")

        user_respons = chatGPTClass.ask_query(
            chatGPTClass.tabs_window_handles[-2], gpt_respons, file_address=file_address
        )
        user_asking = False
        
    else:
        print("Assistant_________________________________________________________")

        if "Reuploading..." in user_respons:
            file_address = file_address_Backup

        gpt_respons = chatGPTClass.ask_query(
            chatGPTClass.tabs_window_handles[-1],
            user_respons,
            file_address=file_address,
        )
        user_asking = True
        file_address = ""
