# Initialize prompts
# safe girl
# prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),(photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),<lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,<lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>,(1girl ),(16yo),(long hair),(skinny:1.31),thin legs,upper body,dress,slender_waist,medium breasts,parted_lips"

prompts = "best quality.masterpiece,highres,available,light,realistic,photo_(medium),reality.,\
<lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,<lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>,\
1girl,skinny,slender,\
long hair,medium breasts,slender_waist,\
off-shoulder_dress,thighhighs,\
standing,"

negative_prompts = "((naked,nude,nsfw)),ng_deepnegative_v1_75t,easynegative,paintings,sketches,(worst quality, low quality:1.4),(normal quality:2),lowres,normal quality,((monochrome)),((grayscale)),(duplicate:1.331),(morbid:1.21),(mutilated:1.21),(tranny:1.331),(missing arms:1.331),(extra arms:1.331),no legs,(extra legs:1.331),extra limbs,extra digit,bad hands,bad fingers,extra fingers,(too many fingers:1.61051),missing fingers,deformed fingers,mutated hands,(fused fingers:1.61051),(poorly drawn hands:1.331),(bad anatomy:1.21),bad body,(disfigured:1.331),(bad proportions:1.331),(more than 2 nipples:1.331),skin spots,watermarks,texts,artist name,logo,acnes,skin blemishes,age spot,(outdoor:1.6),manboobs,horror,(fat ass),(bad-artist:0.7),"

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

# marginal girl
# prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),(photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),<lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,<lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>,(1girl ),(16yo),(long hair),(skinny:1.31),thin legs,upper body,slender_waist,medium breasts,parted_lips,stirrup_legwear,black_thighhighs,a slender hand,the hand of details,the right hand,"

# negative_prompts = ",ng_deepnegative_v1_75t,easynegative,paintings,sketches,(worst quality, low quality:1.4),(normal quality:2),lowres,normal quality,((monochrome)),((grayscale)),(duplicate:1.331),(morbid:1.21),(mutilated:1.21),(tranny:1.331),(missing arms:1.331),(extra arms:1.331),no legs,(extra legs:1.331),extra limbs,extra digit,bad hands,bad fingers,extra fingers,(too many fingers:1.61051),missing fingers,deformed fingers,mutated hands,(fused fingers:1.61051),(poorly drawn hands:1.331),(bad anatomy:1.21),bad body,(disfigured:1.331),(bad proportions:1.331),(more than 2 nipples:1.331),skin spots,watermarks,texts,artist name,logo,acnes,skin blemishes,age spot,(outdoor:1.6),manboobs,horror,(fat ass),(bad-artist:0.7),"

# ad_prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),\
#     (photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),\
#     <lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,\
#     <lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>"

# adetailer = {
#     "ADetailer": {
#       "args": [
#         {
#           "ad_model": "face_yolov8n.pt",
#           "ad_prompt": ad_prompts,
#           "ad_negative_prompt": "",
#           "ad_confidence": 0.3,
#         }
#       ]
#     }
#   }

negative_prompts = "EasyNegative,bad-artist-anime,letter box,bad-artist bad-hands-5,badhandv4,bad_prompt_version2,ng_deepnegative_v1_75t,bad-picture-chill-75v,[badhandv4],verybadimagenegative_v1.3,sketch by bad-artist,((((ugly)))),(((duplicate))),((morbid)),((mutilated)),[out of frame],extra fingers,mutated hands,three legs:1.2,three hands:1.2,((poorly drawn hands)),((poorly drawn face)),(((mutation))),(((deformed))),((ugly)),blurry,((bad anatomy)),(((bad proportions))),((extra limbs)),cloned face,(((disfigured))). out of frame,ugly,extra limbs,(bad anatomy),gross proportions,(malformed limbs),((missing arms)),((missing legs)),(((extra arms))),(((extra legs))),mutated hands,(fused fingers),(too many fingers),(((long neck))),signature,text,facial hair,loli,chibi,disabled body,DeepNegative,(jeans:1.2),"