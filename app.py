from typing import List
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5,
)

prompt_template = PromptTemplate(
    input_variables=["name", "story"],
    template="""
                
                You are a professional story writer for short form video content where the video will be created with a minimum of 10 scenes. You write the scenes for the story given by the user. The video that will be generated will comprise of images with animations and audio telling the story.

                The scene will be an array which will consist of image_prompt and audio_text of all the scenes like a json file of each scene.
                You need to write the audio_text of the scene in such a way that it will be a continuation of the previous scene audio_text so that the story will be continuous. The images need not be continous but should atleast be a little related to the scene.

                The scene will consist of a image with small animations like zoom in, zoom out, pan, etc. The audio will be a voice over of the text of the scene.
                The image that will be displayed will be generated by ai with the image_prompt from the scene. The audio will be generated from the audio_text from the scene.

                Each scene should be too long and each scene will be of the length of the audio_text. That is you need to generate the audio_text of each scene with 10-15 words and not more, so structure the scenes accordingly.

                You as the scene writer for the story needs to write a description for the image to be generated by ai and also you need to wite short audio overlays for the scene being delivered at the moment.
                So you need to think about the how many scenes should be there and how to structure them properly and how you need to write the image_prompt for the scene and how you need to write the audio_text for the scene.

                The output should be a json object with the scenes array which will consist of image_prompt and audio_text of all the scenes.
                
                Ensure the response is valid JSON and can be parsed by Python's json.loads() function.
                Do not include any additional text outside the JSON object.
                

                name of the story given by the user: {name}
                story given by the user: {story}
                Answer:""")




class Scene:
    index: int
    image_prompt: str
    audio_text: str
    image_file: str | None
    audio_file: str | None


class Project:
    name: str
    story: str
    scenes: List[Scene]


def create_scenes(prompt_template):
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.invoke({
                "name": "fear at night",
                "story": "A boy sleeping on his bed at night wanted to drink water, so he went to fridge and while taking water from the fridge something fell on top of him, so he ran to his bed but felt that something maybe sleeping in his sheets. so he went under the bed to sleep but then there is a hgost there, and then he suddenly woke from his dream and realised that it was just a dream."
            })
    
    raw_response = response['text'].strip()
    

    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3].strip()
    
    try:
        response_json = json.loads(raw_response)
        scenes_data = response_json.get("scenes", [])


        scenes = []
        for idx, scene_data in enumerate(scenes_data, start=1):
            scene = Scene()
            scene.index = idx
            scene.image_prompt = scene_data.get("image_prompt", "")
            scene.audio_text = scene_data.get("audio_text", "")
            scenes.append(scene)
        

        project = Project()
        project.name = "fear at night"
        project.story = "A boy sleeping on his bed..."
        project.scenes = scenes
        
        # Optional: Print or return the results
        print(f"Created project with {len(scenes)} scenes:")
        for scene in scenes:
            print(f"Scene {scene.index}:")
            print(f"Image prompt: {scene.image_prompt}")
            print(f"Audio text: {scene.audio_text}\n")
        
        return project
        
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    except Exception as e:
        print(f"Error processing response: {e}")
    # print(response)
    # format_res = response['text'].strip()
    # if format_res.startswith("json") and format_res.endswith(""):
    #     format_res = format_res[7:-3].strip()
    # try:
    #     response_json = json.loads(format_res)
    #     print("Formatted res JSON - ", response_json)
    # except json.JSONDecodeError as e:
    #             print(f"JSON Decode Error: {e}")


create_scenes(prompt_template)

def create_images():
    pass


def create_audio():
    pass


def image_to_video_with_captions_overlay_and_audio():
    pass


def merge_video_scenes():
    pass


def main():
    pass


'''
    get story name and story from user
    create scenes using ai
    create images using ai
    create audio using gtts
    merge images, audio and captions to single scene 
    merge all scenes to single video
'''

if __name__ == "__main__":
    main()



