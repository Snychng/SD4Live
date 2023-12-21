# Initialize prompts
prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),(photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),<lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,<lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>,(1girl ),(16yo),(long hair),(skinny:1.31),thin legs,upper body,slender_waist,medium breasts,parted_lips,stirrup_legwear,black_thighhighs,a slender hand,the hand of details,the right hand,"

negative_prompts = "ng_deepnegative_v1_75t,easynegative,paintings,sketches,(worst quality, low quality:1.4),(normal quality:2),lowres,normal quality,((monochrome)),((grayscale)),(duplicate:1.331),(morbid:1.21),(mutilated:1.21),(tranny:1.331),(missing arms:1.331),(extra arms:1.331),no legs,(extra legs:1.331),extra limbs,extra digit,bad hands,bad fingers,extra fingers,(too many fingers:1.61051),missing fingers,deformed fingers,mutated hands,(fused fingers:1.61051),(poorly drawn hands:1.331),(bad anatomy:1.21),bad body,(disfigured:1.331),(bad proportions:1.331),(more than 2 nipples:1.331),skin spots,watermarks,texts,artist name,logo,acnes,skin blemishes,age spot,(outdoor:1.6),manboobs,horror,(fat ass),(bad-artist:0.7),"

ad_prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),\
    (photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),\
    <lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,\
    <lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>"

adetailer = {
    "ADetailer": {
      "args": [
        {
          "ad_model": "face_yolov8n.pt",
          "ad_prompt": ad_prompts,
          "ad_negative_prompt": "",
          "ad_confidence": 0.3,
        }
      ]
    }
  }