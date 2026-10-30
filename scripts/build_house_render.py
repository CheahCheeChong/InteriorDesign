# Warm-style house render — rebuilds the SketchUp model in Blender and renders views.
# Run inside Blender:  exec(open("<this file>").read())
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

OUT = '/Users/cheahcheechong/Desktop/House_Render'
IN = 0.0254
MATS_TXT = 'Floor_Warm_Oak=0,196,152,106,255;Floor_Concrete=1,150,150,152,255;Floor_Travertine=2,214,196,170,255;Floor_Warm_Terrazzo=3,222,208,188,255;Deck_Teak=4,160,110,68,255;Glass=5,170,205,225,70;AC_Unit_White=6,228,228,224,255;Ceiling_Warm_White=7,248,243,234,255;Light_Oak=8,205,168,120,255;Brushed_Brass=9,196,160,92,255;Walnut=10,95,62,40,255;Black_Frame=11,32,30,30,255;Frame_Bronze=12,92,76,62,255;Boucle_Sand=13,208,192,168,255;Boucle_Oatmeal=14,226,214,194,255;Cushion_Rust=15,160,82,50,255;Olive_Green=16,120,124,76,255;Terracotta_Fabric=17,178,96,64,255;Rug_Jute=18,196,172,132,255;Ceramic_Cream=19,236,226,208,255;Lamp_Shade_Linen=20,240,228,205,255;Terracotta_Pot=21,176,104,70,255;TV_Black=22,22,22,24,255;Warm_Light=23,255,226,170,255;Linen_Curtain=24,232,222,204,255;Aircond_White=25,244,242,238,255;Art_Ochre=26,204,150,82,255;Rattan=27,186,142,88,255;Cane_Seat=28,214,186,140,255;Art_Clay=29,186,120,92,255;Porcelain_White=30,250,250,250,255;Appliance_Steel=31,150,150,148,255;Quartz_Warm_White=32,240,234,224,255;Zellige_Terracotta=33,196,132,96,255;Cabinet_Cream=34,236,226,206,255;Cabinet_Sage=35,156,162,128,255;Plant_Green=36,86,128,72,255;Bedding_Clay=37,196,150,120,255;Bedding_Ivory=38,242,236,224,255;Bedding_Sage=39,170,176,144,255;Tile_Warm_Beige=40,226,212,190,255;Limewash_Clay=41,210,180,150,255;Rug_Oatmeal_Wool=42,220,208,188,255;Travertine_Wall=43,220,202,176,255;Teak_Outdoor=44,150,100,60,255'
PART1 = '0|b|T0,120,-2|0,0,0,100,120,2|\n0|b|T0,240,-2|0,0,0,144,108,2|\n1|b|T0,348,-2|0,0,0,62,97,2|\n2|b|T62,348,-2|0,0,0,82,69,2|\n0|b|T62,417,-2|0,0,0,130,136,2|\n0|b|T144,348,-2|0,0,0,48,69,2|\n2|b|T100,120,-2|0,0,0,92,72,2|\n3|b|T100,0,-2|0,0,0,176,120,2|\n3|b|T192,120,-2|0,0,0,84,72,2|\n0|b|T276,0,-2|0,0,0,64,192,2|\n0|b|T144,240,-2|0,0,0,48,108,2|\n0|b|T192,192,-2|0,0,0,148,327,2|\n4|b|T192,519,-2|0,0,0,148,61,2|\n0|b|T100,192,-2|0,0,0,44,48,2|\n0|b|T144,192,-2|0,0,0,48,48,2|\n5|b|T-0.5,150,36|0,0,0,1,60,48|\n5|b|T-0.5,264,36|0,0,0,1,60,48|\n5|b|T191.5,132,70|0,0,0,1,28,20|\n5|b|T112,-0.5,40|0,0,0,84,1,44|\n5|b|T214,-0.5,44|0,0,0,48,1,32|\n5|b|T222,518.5,0|0,0,0,88,1,84|\n5|b|T92,552.5,30|0,0,0,76,1,60|\n6|b|T6,360,0|0,0,0,32,12,24|\n6|b|T6,380,0|0,0,0,32,12,24|\n6|b|T6,400,0|0,0,0,32,12,24|\n6|b|T6,420,0|0,0,0,32,12,24|\n7|b|T0,0,102|0,0,0,340,348,4|\n7|b|T62,348,102|0,0,0,278,171,4|\n7|b|T62,519,102|0,0,0,130,34,4|\n8|b|T143.25,304.25,0|0,0,0,1.5,35.5,79.75|\n9|b|T141.75,336,36|0,0,0,3,1,1|\n10|b|T140.5,301.5,0|0,0,0,1,2.5,80|\n10|b|T140.5,340,0|0,0,0,1,2.5,80|\n10|b|T140.5,301.5,80|0,0,0,1,41,2.5|\n10|b|T146.5,301.5,0|0,0,0,1,2.5,80|\n10|b|T146.5,340,0|0,0,0,1,2.5,80|\n10|b|T146.5,301.5,80|0,0,0,1,41,2.5|\n8|b|T143.25,376.25,0|0,0,0,1.5,35.5,79.75|\n9|b|T141.75,408,36|0,0,0,3,1,1|\n10|b|T140.5,373.5,0|0,0,0,1,2.5,80|\n10|b|T140.5,412,0|0,0,0,1,2.5,80|\n10|b|T140.5,373.5,80|0,0,0,1,41,2.5|\n10|b|T146.5,373.5,0|0,0,0,1,2.5,80|\n10|b|T146.5,412,0|0,0,0,1,2.5,80|\n10|b|T146.5,373.5,80|0,0,0,1,41,2.5|\n10|b|T290.25,-0.75,0|0,0,0,35.5,1.5,81.75|\n9|b|T322,-2.25,36|0,0,0,1,3,1|\n10|b|T287.5,-3.5,0|0,0,0,2.5,1,82|\n10|b|T326,-3.5,0|0,0,0,2.5,1,82|\n10|b|T287.5,-3.5,82|0,0,0,41,1,2.5|\n10|b|T287.5,2.5,0|0,0,0,2.5,1,82|\n10|b|T326,2.5,0|0,0,0,2.5,1,82|\n10|b|T287.5,2.5,82|0,0,0,41,1,2.5|\n8|b|T150.25,191.25,0|0,0,0,35.5,1.5,79.75|\n9|b|T182,189.75,36|0,0,0,1,3,1|\n10|b|T147.5,188.5,0|0,0,0,2.5,1,80|\n10|b|T186,188.5,0|0,0,0,2.5,1,80|\n10|b|T147.5,188.5,80|0,0,0,41,1,2.5|\n10|b|T147.5,194.5,0|0,0,0,2.5,1,80|\n10|b|T186,194.5,0|0,0,0,2.5,1,80|\n10|b|T147.5,194.5,80|0,0,0,41,1,2.5|\n8|b|T150.25,347.25,0|0,0,0,35.5,1.5,79.75|\n9|b|T182,345.75,36|0,0,0,1,3,1|\n10|b|T147.5,344.5,0|0,0,0,2.5,1,80|\n10|b|T186,344.5,0|0,0,0,2.5,1,80|\n10|b|T147.5,344.5,80|0,0,0,41,1,2.5|\n10|b|T147.5,350.5,0|0,0,0,2.5,1,80|\n10|b|T186,350.5,0|0,0,0,2.5,1,80|\n10|b|T147.5,350.5,80|0,0,0,41,1,2.5|\n5|b|T206.5,191.5,0|0,0,0,37,1,83.5|\n11|b|T206,190.5,0|0,0,0,2,3,84|\n11|b|T242,190.5,0|0,0,0,2,3,84|\n11|b|T206,190.5,82|0,0,0,38,3,2|\n11|b|T208,191,40|0,0,0,34,2,1.5|\n12|b|T-1,150,36|0,0,0,2,1.5,48|\n12|b|T-1,208.5,36|0,0,0,2,1.5,48|\n12|b|T-1,150,36|0,0,0,2,60,1.5|\n12|b|T-1,150,82.5|0,0,0,2,60,1.5|\n12|b|T-1,179.25,36|0,0,0,2,1.5,48|\n8|b|T2.5,148,35|0,0,0,4,64,1|\n12|b|T-1,264,36|0,0,0,2,1.5,48|\n12|b|T-1,322.5,36|0,0,0,2,1.5,48|\n12|b|T-1,264,36|0,0,0,2,60,1.5|\n12|b|T-1,264,82.5|0,0,0,2,60,1.5|\n12|b|T-1,293.25,36|0,0,0,2,1.5,48|\n8|b|T2.5,262,35|0,0,0,4,64,1|\n12|b|T191,132,70|0,0,0,2,1.5,20|\n12|b|T191,158.5,70|0,0,0,2,1.5,20|\n12|b|T191,132,70|0,0,0,2,28,1.5|\n12|b|T191,132,88.5|0,0,0,2,28,1.5|\n12|b|T191,145.25,70|0,0,0,2,1.5,20|\n8|b|T185.5,130,69|0,0,0,4,32,1|\n12|b|T112,-1,40|0,0,0,1.5,2,44|\n12|b|T194.5,-1,40|0,0,0,1.5,2,44|\n12|b|T112,-1,40|0,0,0,84,2,1.5|\n12|b|T112,-1,82.5|0,0,0,84,2,1.5|\n12|b|T153.25,-1,40|0,0,0,1.5,2,44|\n8|b|T110,2.5,39|0,0,0,88,4,1|\n12|b|T214,-1,44|0,0,0,1.5,2,32|\n12|b|T260.5,-1,44|0,0,0,1.5,2,32|\n12|b|T214,-1,44|0,0,0,48,2,1.5|\n12|b|T214,-1,74.5|0,0,0,48,2,1.5|\n12|b|T237.25,-1,44|0,0,0,1.5,2,32|\n8|b|T212,2.5,43|0,0,0,52,4,1|\n12|b|T92,552,30|0,0,0,1.5,2,60|\n12|b|T166.5,552,30|0,0,0,1.5,2,60|\n12|b|T92,552,30|0,0,0,76,2,1.5|\n12|b|T92,552,88.5|0,0,0,76,2,1.5|\n12|b|T129.25,552,30|0,0,0,1.5,2,60|\n8|b|T90,546.5,29|0,0,0,80,4,1|\n12|b|T222,518,0|0,0,0,2,2,84|\n12|b|T265,518,0|0,0,0,2,2,84|\n12|b|T308,518,0|0,0,0,2,2,84|\n12|b|T222,518,82|0,0,0,88,2,2|\n8|b|T143.25,200.25,0|0,0,0,1.5,35.5,79.75|\n9|b|T141.75,232,36|0,0,0,3,1,1|\n10|b|T140.5,197.5,0|0,0,0,1,2.5,80|\n10|b|T140.5,236,0|0,0,0,1,2.5,80|\n10|b|T140.5,197.5,80|0,0,0,1,41,2.5|\n10|b|T146.5,197.5,0|0,0,0,1,2.5,80|\n10|b|T146.5,236,0|0,0,0,1,2.5,80|\n10|b|T146.5,197.5,80|0,0,0,1,41,2.5|\n10|b|T296.25,191.25,0|0,0,0,37.5,1.5,83.75|\n9|b|T300,189.75,36|0,0,0,1,3,1|\n10|b|T293.5,188.5,0|0,0,0,2.5,1,84|\n10|b|T334,188.5,0|0,0,0,2.5,1,84|\n10|b|T293.5,188.5,84|0,0,0,43,1,2.5|\n10|b|T293.5,194.5,0|0,0,0,2.5,1,84|\n10|b|T334,194.5,0|0,0,0,2.5,1,84|\n10|b|T293.5,194.5,84|0,0,0,43,1,2.5|\n10|b|T300,189.3,46|0,0,0,30,1,32|\n10|b|T300,189.3,8|0,0,0,30,1,32|\n10|b|T300,193.7,46|0,0,0,30,1,32|\n10|b|T300,193.7,8|0,0,0,30,1,32|\n10|r|T196,395,0|0,0,0,34,92,4|1\n13|r|T194.5,393,4|0,0,0,36,96,12|3\n13|r|T194.5,393,16|0,0,0,10,96,16|4\n13|r|T194.5,481,16|0,0,0,36,8,9|3.5\n14|r|T204,394,16|0,0,0,26,28.5,6|3\n14|r|T202,395,22|0,0,0,9,27,16|4\n14|r|T204,423,16|0,0,0,26,28.5,6|3\n14|r|T202,424,22|0,0,0,9,27,16|4\n14|r|T204,452,16|0,0,0,26,28.5,6|3\n14|r|T202,453,22|0,0,0,9,27,16|4\n13|r|T230.5,393,4|0,0,0,32,32,12|3\n14|r|T231,394,16|0,0,0,31,30,6|3\n15|r|T205,470,22|0,0,0,5,16,15|2.49\n16|r|T205,400,22|0,0,0,5,16,15|2.49\n17|r|T232,395,22|0,0,0,26,14,1.5|0.7\n18|r|T236,385,0|0,0,0,86,118,0.4|6\n10|c|T282,446,13|-19,-19,0,19,19,2|0:19;2:19\n10|c|T282,446,0|-12,-12,0,12,12,13|0:12;13:12\n19|c|T280,448,15|-6,-6,0,6,6,3|0:3;3:6\n10|c|T206,384,21|-8,-8,0,8,8,1.5|0:8;1.5:8\n9|c|T206,384,0|-2,-2,0,2,2,21|0:2;21:1.2\n9|c|T206,500,0|-6,-6,0,6,6,1|0:6;1:6\n9|c|T206,500,1|-0.5,-0.5,0,0.5,0.5,55|0:0.5;55:0.5\n20|c|T206,500,52|-9,-9,0,9,9,12|0:9;12:7\n17|r|M-1,0,0,-0,-1,0,0,0,1,300,503,6|0,0,0,30,30,10|5\n17|r|M-1,0,0,-0,-1,0,0,0,1,300,481,16|0,0,0,30,8,16|3.99\n17|r|M-1,0,0,-0,-1,0,0,0,1,300,503,16|0,0,0,5,30,8|2.49\n17|r|M-1,0,0,-0,-1,0,0,0,1,275,503,16|0,0,0,5,30,8|2.49\n10|r|M-1,0,0,-0,-1,0,0,0,1,298,501,0|0,0,0,2,2,6|0.06\n10|r|M-1,0,0,-0,-1,0,0,0,1,274,501,0|0,0,0,2,2,6|0.06\n10|r|M-1,0,0,-0,-1,0,0,0,1,298,477,0|0,0,0,2,2,6|0.06\n10|r|M-1,0,0,-0,-1,0,0,0,1,274,477,0|0,0,0,2,2,6|0.06\n21|c|T327,509,0|-8,-8,0,8,8,14|0:6;14:8\n10|c|T327,509,14|-0.8,-0.8,0,0.8,0.8,26|0:0.8;26:0.6\n16|c|T327,509,38|-12,-12,0,12,12,30|0:3;6:11;16:12;26:6;30:1\nFLUTE\n8|r|T322,398,10|0,0,0,15,88,12|1\n22|r|T334.5,414,40|0,0,0,1.5,57,32|0.06\n23|r|T335,380,95|0,0,0,2,122,1|0.06\n8|r|T320,343,0|0,0,0,17.5,32,72|0.5\n19|r|T324,350,50|0,0,0,6,6,8|0.06\n19|r|T324,358,50|0,0,0,6,6,10|0.06\n19|r|T324,366,50|0,0,0,6,6,12|0.06\n24|r|T210,512,0|0,0,0,28,3,100|0.06\n24|r|T294,512,0|0,0,0,28,3,100|0.06\n9|r|T208,513,100|0,0,0,116,2,1|0.06\n9|c|T265,445,88|-4,-4,0,4,4,6|0:4;6:3\n10|r|T268,442.5,90|0,0,0,26,5,0.5|2\n10|r|M-0.5,0.866,0,-0.866,-0.5,0,0,0,1,265.67,448.85,90|0,0,0,26,5,0.5|2\n10|r|M-0.5,-0.866,0,0.866,-0.5,0,0,0,1,261.33,443.65,90|0,0,0,26,5,0.5|2\n25|r|T248,509,84|0,0,0,36,9,12|2\n10|r|T195,418,46|0,0,0,1,40,28|0.06\n26|r|T195.6,420,48|0,0,0,0.5,36,24|0.06\n8|r|T208,255,28.5|0,0,0,72,38,1.5|3\n8|r|T214,260,0|0,0,0,2.5,2.5,28.5|1\n8|r|T274,260,0|0,0,0,2.5,2.5,28.5|1\n8|r|T214,287,0|0,0,0,2.5,2.5,28.5|1\n8|r|T274,287,0|0,0,0,2.5,2.5,28.5|1\n8|r|T216,261,25|0,0,0,58,1,3.5|0.06\n8|r|T216,288,25|0,0,0,58,1,3.5|0.06\n22|c|T228,274,70|-0.2,-0.17,0,0.2,0.17,32|0:0.2;32:0.2\n27|c|T228,274,58|-9,-9,0,9,9,12|0:9;5:8.5;10:6;12:2\n22|c|T260,274,70|-0.2,-0.17,0,0.2,0.17,32|0:0.2;32:0.2\n27|c|T260,274,58|-9,-9,0,9,9,12|0:9;5:8.5;10:6;12:2\n10|r|T321,236,6|0,0,0,16.5,76,26|1\n9|r|T323,238,0|0,0,0,1.5,2,6|0.06\n9|r|T323,308,0|0,0,0,1.5,2,6|0.06\n21|c|T329,250,32|-4,-4,0,4,4,16|0:3;10:4;16:2\n19|c|T329,262,32|-5,-5,0,5,5,8|0:2;4:5;8:2\n9|c|M0,0,1,0,1,0,-1,0,0,337.5,274,60|-15,-15,0,15,15,0.8|0:15;0.8:15\nCHAIRS\n8|r|T146.5,252,0|0,0,0,16,34,32|1\n29|r|T147,256,42|0,0,0,1,26,30|0.06\n8|r|T321.5,30,8|0,0,0,16,72,34|1\n23|r|T322,31,7.5|0,0,0,15,70,0.5|0.06\n10|r|T280,40,0|0,0,0,15,40,18|1.5\n14|r|T280.5,41,18|0,0,0,14,38,2.5|1.2\n9|c|M0,0,1,0,1,0,-1,0,0,337.5,66,62|-13,-13,0,13,13,0.8|0:13;0.8:13\n20|c|T308,70,84|-5,-5,0,5,5,8|0:5;8:5\n18|r|T284,10,0|0,0,0,40,120,0.4|3\nSKIRT\n'
PART2 = '10|r|T103.5,3.5,0|0,0,0,169,22,4|0.06\n10|r|T250.5,26.5,0|0,0,0,22,73,4|0.06\n8|r|T132.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T140.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T153.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T161.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T174.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T182.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T195.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T203.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T216.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T224.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T237.5,2.5,4|0,0,0,20.8,23.5,30.5|0.4\n9|r|T245.5,25.9,31|0,0,0,5,0.6,0.6|0.06\n8|r|T102.5,2.5,4|0,0,0,30,23.5,30.5|0.4\n8|r|T249.5,26.5,4|0,0,0,23.5,18.2,30.5|0.4\n9|r|T249,33.5,31|0,0,0,0.6,5,0.6|0.06\n8|r|T249.5,44.8,4|0,0,0,23.5,18.2,30.5|0.4\n9|r|T249,51.8,31|0,0,0,0.6,5,0.6|0.06\n8|r|T249.5,63.1,4|0,0,0,23.5,18.2,30.5|0.4\n9|r|T249,70.1,31|0,0,0,0.6,5,0.6|0.06\n8|r|T249.5,81.4,4|0,0,0,23.5,18.2,30.5|0.4\n9|r|T249,88.4,31|0,0,0,0.6,5,0.6|0.06\n30|r|T104.5,3.5,4|0,0,0,26,22,29|0.06\n31|c|M1,0,0,0,0,1,0,-1,0,117.5,26,20|-6,-6,0,6,6,0.8|0:6;0.8:6\n32|r|T102.5,2.5,34.5|0,0,0,171,25,1.5|0.4\n32|r|T248.5,27.5,34.5|0,0,0,25,72.5,1.5|0.4\n33|r|T132.5,2.5,36|0,0,0,141,0.5,18|0.06\n33|r|T273,27.5,36|0,0,0,0.5,72,18|0.06\n22|r|T224,7,35.8|0,0,0,24,16,0.4|2\n9|c|T236,5,36|-0.6,-0.6,0,0.6,0.6,13|0:0.6;13:0.5\n22|r|T253,46,36|0,0,0,20,28,0.4|0.06\n34|r|T255,44,62|0,0,0,18,32,18|1\n34|r|T261.5,27.5,54|0,0,0,12,16.5,36|0.4\n34|r|T261.5,76,54|0,0,0,12,24,36|0.4\n34|r|T262,2.5,54|0,0,0,11.5,12,36|0.4\n34|r|T196,2.5,54|0,0,0,18,12,36|0.4\n8|r|T102.5,40,56|0,0,0,10,50,1.25|0.06\n8|r|T102.5,40,70|0,0,0,10,50,1.25|0.06\n19|c|T106,60,71.25|-2.2,-2.2,0,2.2,2.2,6|0:2.2;6:2.2\n19|c|T112,60,71.25|-2.2,-2.2,0,2.2,2.2,9|0:2.2;9:2.2\n19|c|T118,60,71.25|-2.2,-2.2,0,2.2,2.2,7|0:2.2;7:2.2\n35|r|T249.5,100,0|0,0,0,24,22.3,96|0.4\n9|r|T249,110.95,32|0,0,0,0.6,0.6,30|0.06\n35|r|T249.5,122.5,0|0,0,0,24,22.3,96|0.4\n9|r|T249,133.45,32|0,0,0,0.6,0.6,30|0.06\n35|r|T249.5,145,0|0,0,0,24,22.3,96|0.4\n9|r|T249,155.95,32|0,0,0,0.6,0.6,30|0.06\n35|r|T249.5,167.5,0|0,0,0,24,21.8,96|0.4\n9|r|T249,178.2,32|0,0,0,0.6,0.6,30|0.06\n35|r|T148,58,0|0,0,0,60,26,34.5|0.5\n32|r|T146,56,34.5|0,0,0,64,34,1.5|1.5\n28|c|T160,98,24|-7.5,-7.5,0,7.5,7.5,2|0:7.5;2:7.5\n8|c|T155,93,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T165,93,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T155,103,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T165,103,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n28|c|T194,98,24|-7.5,-7.5,0,7.5,7.5,2|0:7.5;2:7.5\n8|c|T189,93,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T199,93,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T189,103,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n8|c|T199,103,0|-0.7,-0.7,0,0.7,0.7,24|0:0.7;24:0.6\n22|c|T166,72,72|-0.2,-0.17,0,0.2,0.17,30|0:0.2;30:0.2\n9|c|T166,72,62|-6,-6,0,6,6,11|0:1;3:5;6:6;9:5;11:1.5\n22|c|T190,72,72|-0.2,-0.17,0,0.2,0.17,30|0:0.2;30:0.2\n9|c|T190,72,62|-6,-6,0,6,6,11|0:1;3:5;6:6;9:5;11:1.5\n18|r|T140,34,0|0,0,0,76,18,0.4|2\n21|c|T268,10,36|-3,-3,0,3,3,5|0:2.5;5:3\n36|c|T268,10,41|-4,-4,0,4,4,8|0:3;5:4;8:1\n8|r|T2.5,122.5,4|0,0,0,80,42,8|1\n10|r|T4.5,124.5,0|0,0,0,76,38,4|0.06\n37|r|T2.5,122.5,12|0,0,0,4,42,26|1.8\n38|r|T6.5,123.5,12|0,0,0,75,40,8|2\n39|r|T30,123,18.5|0,0,0,53,41,3|1.4\n38|r|T8,128,20|0,0,0,14,30,4.5|2.2\n8|r|T2.5,172,28|0,0,0,22,58,1.5|0.6\n10|r|T18,173,0|0,0,0,1.5,1.5,28|0.06\n10|r|T18,227.5,0|0,0,0,1.5,1.5,28|0.06\n8|r|T2.5,205,21|0,0,0,20,24,7|0.06\n28|r|T30,192,17|0,0,0,18,18,2|2\n8|r|T46,193,19|0,0,0,2,16,14|0.8\n8|r|T31,193,0|0,0,0,1.4,1.4,17|0.06\n8|r|T45,193,0|0,0,0,1.4,1.4,17|0.06\n8|r|T31,207,0|0,0,0,1.4,1.4,17|0.06\n8|r|T45,207,0|0,0,0,1.4,1.4,17|0.06\n34|r|T30,213.5,0|0,0,0,34,24,90|0.5\n9|r|T46,213,36|0,0,0,0.6,0.6,18|0.06\n9|r|T48,213,36|0,0,0,0.6,0.6,18|0.06\n24|r|T3,148,62|0,0,0,2,64,24|0.06\n8|r|T2.5,178,50|0,0,0,8,46,1|0.06\n18|r|T30,168,0|0,0,0,44,40,0.4|19\n20|c|T50,180,80|-9,-9,0,9,9,18|0:2;4:8;10:9;16:6;18:1\n25|r|T2.5,170,86|0,0,0,9,32,11|2\n8|b|T102.5,194.5,0|0,0,0,12,36,60|\n37|b|T112,222,0|0,0,0,18,13,6|\n10|r|T2.5,242.5,4|0,0,0,80,42,8|1\n22|r|T4.5,244.5,0|0,0,0,76,38,4|0.06\n14|r|T2.5,242.5,12|0,0,0,4,42,26|1.8\n38|r|T6.5,243.5,12|0,0,0,75,40,8|2\n15|r|T30,243,18.5|0,0,0,53,41,3|1.4\n38|r|T8,248,20|0,0,0,14,30,4.5|2.2\n10|r|T20,321.5,28|0,0,0,56,24,1.5|0.6\n22|r|T21,323,0|0,0,0,1.5,21,28|0.06\n22|r|T73.5,323,0|0,0,0,1.5,21,28|0.06\n22|r|T34,340,33|0,0,0,28,1.5,16|0.06\n22|r|T47,337,29.5|0,0,0,2,3,4|0.06\n14|r|T39,298,17|0,0,0,20,20,3|4\n14|r|T40,296,20|0,0,0,18,3,18|1.4\n22|c|T49,308,0|-1,-0.95,0,1,0.95,17|0:1;17:1\n22|c|T49,308,0|-11,-10.46,0,11,10.46,1.5|0:11;1.5:11\n8|r|T82,330,0|0,0,0,1,15.5,76|0.06\n8|r|T111,330,0|0,0,0,1,15.5,76|0.06\n8|r|T82,330,0|0,0,0,30,15.5,1|0.06\n8|r|T82,330,18.75|0,0,0,30,15.5,1|0.06\n8|r|T82,330,37.5|0,0,0,30,15.5,1|0.06\n8|r|T82,330,56.25|0,0,0,30,15.5,1|0.06\n8|r|T82,330,75|0,0,0,30,15.5,1|0.06\n15|r|T84,333,20|0,0,0,5.5,9,9|0.06\n16|r|T90.5,333,20|0,0,0,5.5,9,10.5|0.06\n37|r|T97,333,20|0,0,0,5.5,9,12|0.06\n34|r|T103.5,333,20|0,0,0,5.5,9,9|0.06\n15|r|T84,333,38.75|0,0,0,5.5,9,10.5|0.06\n16|r|T90.5,333,38.75|0,0,0,5.5,9,12|0.06\n37|r|T97,333,38.75|0,0,0,5.5,9,9|0.06\n34|r|T103.5,333,38.75|0,0,0,5.5,9,10.5|0.06\n10|r|T117.5,243,0|0,0,0,24,54,90|0.5\n9|r|T117,268,36|0,0,0,0.6,0.6,18|0.06\n9|r|T117,272,36|0,0,0,0.6,0.6,18|0.06\n24|r|T3,262,62|0,0,0,2,64,24|0.06\n37|r|T40,286,0|0,0,0,60,34,0.4|3\n27|c|T70,294,80|-9,-9,0,9,9,12|0:2;6:9;10:7;12:1\n21|c|T132,334,0|-6,-6,0,6,6,12|0:5;12:6\n36|c|T132,334,12|-9,-9,0,9,9,26|0:4;8:9;18:8;26:2\n25|r|T132,300,86|0,0,0,9,32,11|2\n33|r|T188.5,122.5,0|0,0,0,1,29.5,84|0.06\n33|r|T154,122.5,0|0,0,0,34.5,1,84|0.06\n40|r|T102.5,122.5,0|0,0,0,0.5,67,48|0.06\n5|r|T154,150,0|0,0,0,22,0.5,78|0.06\n9|r|T154,149.5,77|0,0,0,22,1,1|0.06\n9|c|T172,136,82|-5,-5,0,5,5,0.8|0:5;0.8:5\n9|c|T172,124,40|-0.5,-0.5,0,0.5,0.5,43|0:0.5;43:0.5\n30|r|T110,122.5,0|0,0,0,18,7,31|0.06\n30|r|T111,129.5,0|0,0,0,16,20,15.5|6\n8|r|T102.5,158,18|0,0,0,18,26,14|0.5\n32|r|T102.5,158,32|0,0,0,19,26,1|0.5\n30|r|T106,163,33|0,0,0,12,16,4|5\n9|c|T104,171,33|-0.5,-0.5,0,0.5,0.5,8|0:0.5;8:0.5\n9|r|T103,160,42|0,0,0,1,22,28|0.49\n5|r|T103.5,161,43|0,0,0,0.5,20,26|0.06\n9|r|T140,189,48|0,0,0,14,0.6,0.6|0.06\n37|r|T141,188,30|0,0,0,12,1.5,18|0.06\n20|c|T130,165,86|-4.5,-4.5,0,4.5,4.5,5|0:4;5:4.5\n41|r|T188.5,419.5,0|0,0,0,1,131,102|0.06\nHSLATS\n23|r|T186,438,80|0,0,0,2.5,96,0.6|0.06\n14|r|T106,455,3|0,0,0,80,64,10|2\n22|r|T110,459,0|0,0,0,72,56,3|0.06\n14|r|T181,452,13|0,0,0,5,70,34|2.4\n38|r|T107,456,13|0,0,0,76,62,9|2.5\n38|r|T107,455.5,20|0,0,0,58,63,3|1.5\n17|r|T112,455,23|0,0,0,16,64,1.5|0.7\n38|r|T166,459,22|0,0,0,13,27,6|2.8\n37|r|T174,460,23|0,0,0,7,25,18|3\n38|r|T166,488,22|0,0,0,13,27,6|2.8\n37|r|T174,489,23|0,0,0,7,25,18|3\n15|r|T160,476,22|0,0,0,6,22,9|2.5\n10|r|T168,433,6|0,0,0,18,18,16|1.5\n9|r|T170,435,0|0,0,0,1.2,1.2,6|0.06\n9|r|T183.5,447.5,0|0,0,0,1.2,1.2,6|0.06\n33|c|T177,442,22|-3.5,-3.5,0,3.5,3.5,9|0:3;5:3.5;9:1\n20|c|T177,442,30|-6,-6,0,6,6,8|0:6;8:4.5\n10|r|T168,523,6|0,0,0,18,18,16|1.5\n9|r|T170,525,0|0,0,0,1.2,1.2,6|0.06\n9|r|T183.5,537.5,0|0,0,0,1.2,1.2,6|0.06\n33|c|T177,532,22|-3.5,-3.5,0,3.5,3.5,9|0:3;5:3.5;9:1\n20|c|T177,532,30|-6,-6,0,6,6,8|0:6;8:4.5\n8|r|T64.5,419.5,0|0,0,0,19.1,24,96|0.4\n9|r|T82,443.5,34|0,0,0,0.6,0.6,26|0.06\n8|r|T83.8,419.5,0|0,0,0,19.1,24,96|0.4\n9|r|T84.8,443.5,34|0,0,0,0.6,0.6,26|0.06\n8|r|T103.1,419.5,0|0,0,0,19.1,24,96|0.4\n9|r|T120.6,443.5,34|0,0,0,0.6,0.6,26|0.06\n8|r|T122.4,419.5,0|0,0,0,19.1,24,96|0.4\n9|r|T123.4,443.5,34|0,0,0,0.6,0.6,26|0.06\n17|r|T88,467,0|0,0,0,16,40,17|2\n42|r|T84,446,0|0,0,0,82,82,0.4|4\n14|r|T92,524,7|0,0,0,26,26,9|6\n14|r|T92,524,16|0,0,0,26,7,18|3.49\n10|c|T95,527,0|-0.8,-0.8,0,0.8,0.8,7|0:0.8;7:0.7\n10|c|T113,527,0|-0.8,-0.8,0,0.8,0.8,7|0:0.8;7:0.7\n10|c|T95,545,0|-0.8,-0.8,0,0.8,0.8,7|0:0.8;7:0.7\n10|c|T113,545,0|-0.8,-0.8,0,0.8,0.8,7|0:0.8;7:0.7\n21|c|T72,540,0|-7,-7,0,7,7,14|0:6;14:7\n16|c|T72,540,14|-10,-10,0,10,10,36|0:4;10:10;24:10;36:3\n10|r|T120,531,28|0,0,0,44,18,1.5|0.8\n10|r|T121,532,0|0,0,0,1.5,1.5,28|0.06\n10|r|T161.5,532,0|0,0,0,1.5,1.5,28|0.06\n10|r|T121,546.5,0|0,0,0,1.5,1.5,28|0.06\n10|r|T161.5,546.5,0|0,0,0,1.5,1.5,28|0.06\n19|c|T156,540,29.5|-3,-3,0,3,3,9|0:2;6:3;9:1.5\n24|r|T86,547,0|0,0,0,22,3,100|0.06\n24|r|T152,547,0|0,0,0,22,3,100|0.06\n9|r|T84,548,100|0,0,0,92,2,1|0.06\n27|c|T140,487,88|-12,-12,0,12,12,10|0:3;4:11;8:12;10:10\n25|r|T88,541,86|0,0,0,30,9,11|2\n43|r|T64.5,350.5,0|0,0,0,77,0.6,102|0.06\n43|r|T64.5,351,0|0,0,0,0.6,63.5,102|0.06\n33|r|T65,413.9,0|0,0,0,39,0.6,84|0.06\n10|r|T68,351.1,18|0,0,0,36,20,14|1\n9|r|T68,371,28|0,0,0,36,0.3,0.5|0.06\n43|r|T68,351.1,32|0,0,0,36,20,1.5|1\n30|c|T86,360,33.5|-7.5,-7.5,0,7.5,7.5,5|0:4;2:6.5;5:7.5\n9|c|M1,0,0,0,0,1,0,1,0,86,351.1,56|-11,-11,0,11,11,0.8|0:11;0.8:11\n20|c|T70,352,54|-2.5,-2.5,0,2.5,2.5,6|0:2;6:2.5\n20|c|T102,352,54|-2.5,-2.5,0,2.5,2.5,6|0:2;6:2.5\n43|r|T108,351.1,0|0,0,0,26,7,42|0.5\n9|r|T117,358,36|0,0,0,7,0.4,4|0.06\n30|r|T113,358.1,12|0,0,0,16,21,14|6\n5|r|T104,384,0|0,0,0,0.5,30.5,80|0.06\n9|r|T103.5,384,79|0,0,0,1.5,30.5,1|0.06\n9|c|T84,400,84|-5,-5,0,5,5,0.8|0:5;0.8:5\n9|c|T66,400,40|-0.5,-0.5,0,0.5,0.5,45|0:0.5;45:0.5\n10|r|T65.1,388,44|0,0,0,4,14,1|0.06\n10|r|T139,360,0|0,0,0,1,18,60|0.06\n37|r|T138,361,34|0,0,0,2,16,20|0.06\n38|r|T108,385,0|0,0,0,26,18,0.4|2\n21|c|T135,410,0|-3.5,-3.5,0,3.5,3.5,8|0:3;8:3.5\n36|c|T135,410,8|-5,-5,0,5,5,14|0:2;6:5;14:1\n44|r|T192.5,566,0|0,0,0,147,13,20|1\nSHRUBS\n5|r|T192,579.4,20|0,0,0,148,0.6,22|0.06\n44|r|T192,579,42|0,0,0,148,1.5,1.2|0.06\n18|r|T214,526,0|0,0,0,104,36,0.4|3\n27|r|M-1,0,0,-0,-1,0,0,0,1,245,556,0|0,0,0,26,26,14|8\n27|r|M-1,0,0,-0,-1,0,0,0,1,245,556,14|0,0,0,26,6,14|2.99\n38|r|M-1,0,0,-0,-1,0,0,0,1,242,550,14|0,0,0,20,18,3|3\n27|r|M-1,0,0,-0,-1,0,0,0,1,313,556,0|0,0,0,26,26,14|8\n27|r|M-1,0,0,-0,-1,0,0,0,1,313,556,14|0,0,0,26,6,14|2.99\n38|r|M-1,0,0,-0,-1,0,0,0,1,310,550,14|0,0,0,20,18,3|3\n44|c|T266,542,0|-9,-9,0,9,9,17.5|0:8;16:8;16.01:9;17.5:9\n22|c|T328,532,0|-4,-4,0,4,4,14|0:4;12:4;14:1\n23|c|T328,532,3|-2,-2,0,2,2,6|0:2;6:2\n'
QUICK = False

# ------------------------------------------------------------------ data
def load_mats():
    mats = {}
    for item in MATS_TXT.strip().split(";"):
        name, vals = item.split("=")
        v = [int(x) for x in vals.split(",")]
        mats[v[0]] = (name, (v[1] / 255, v[2] / 255, v[3] / 255), v[4] / 255)
    mats[100] = ("Warm_White_Wall", (244 / 255, 237 / 255, 226 / 255), 1.0)
    return mats

def rotz(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

def P(mat, kind, box, R=None, t=(0, 0, 0), r=0.0, prof=None):
    return dict(mat=mat, kind=kind, box=box, R=R or I3, t=t, r=r, prof=prof)

def bx(m, x, y, z, w, d, h, r=0.0):
    return P(m, "r" if r > 0.2 else "b", (x, y, z, x + w, y + d, z + h), r=r)

def chairs():
    parts = [(28, (-9, -9, 16, 18, 18, 2.5), 2.5), (8, (-9.25, -9.25, 15, 18.5, 18.5, 1), 2.5),
             (8, (-8.5, -8.5, 0, 1.5, 1.5, 15), 0.6), (8, (7, -8.5, 0, 1.5, 1.5, 15), 0.6),
             (8, (-8.5, 7, 0, 1.5, 1.5, 15), 0.6), (8, (7, 7, 0, 1.5, 1.5, 15), 0.6),
             (8, (-8.5, 7, 18.5, 1.5, 1.5, 12), 0.6), (8, (7, 7, 18.5, 1.5, 1.5, 12), 0.6),
             (8, (-9, 6.5, 26, 18, 2, 5), 1.0)]
    out = []
    for (x, y, deg) in [(226, 306, 0), (262, 306, 0), (226, 247, 180), (262, 247, 180), (199, 274, 90), (289, 274, -90)]:
        for (m, (a, b, c, w, d, h), r) in parts:
            out.append(P(m, "r", (a, b, c, a + w, b + d, c + h), R=rotz(deg), t=(x, y, 0), r=r))
    return out

T = 5.0
SK = [("V",0,120,348,[],"+"),("V",62,445,553,[],"+"),("V",100,120,192,[],"both"),("V",100,0,120,[],"+"),
 ("V",144,192,417,[(200,236),(304,340),(376,412)],"both"),("V",192,120,192,[],"both"),("V",192,348,519,[],"both"),
 ("V",192,519,553,[],"-"),("V",276,0,192,[],"both"),("V",340,0,519,[],"-"),
 ("H",0,100,340,[(290,326)],"+"),("H",120,0,100,[],"+"),("H",120,100,192,[],"both"),
 ("H",192,100,276,[(150,186),(206,244)],"both"),("H",192,276,340,[(296,334)],"both"),
 ("H",240,0,144,[],"both"),("H",348,62,144,[],"+"),("H",348,0,62,[],"-"),("H",348,144,192,[(150,186)],"both"),
 ("H",417,62,144,[],"both"),("H",519,192,340,[(222,310)],"-"),("H",553,62,192,[],"-")]

def skirting():
    out = []
    for (o, c, a0, a1, gaps, side) in SK:
        pts = [a0 + 2.5] + [v for g in gaps for v in g] + [a1 - 2.5]
        sides = [-1, 1] if side == "both" else ([1] if side == "+" else [-1])
        for k in range(0, len(pts), 2):
            s0, s1 = pts[k], pts[k + 1]
            if s1 - s0 < 2: continue
            for sg in sides:
                off = c + sg * T / 2 + (0 if sg > 0 else -0.6)
                out.append(bx(10, off, s0, 0, 0.6, s1 - s0, 4) if o == "V" else bx(10, s0, off, 0, s1 - s0, 0.6, 4))
    return out

WALLS = [
 ("V",0,120,348,2.5,[],[(150,210,36,84),(264,324,36,84)],102),
 ("V",62,348,553,2.5,[],[],102),
 ("V",100,0,192,2.5,[],[],102),
 ("V",144,192,417,2.5,[(200,236,80),(304,340,80),(376,412,80)],[],102),
 ("V",192,120,192,2.5,[],[(132,160,70,90)],102),
 ("V",192,348,553,2.5,[],[],102),
 ("V",276,0,192,2.5,[],[],102),
 ("V",340,0,519,2.5,[],[],102),
 ("H",0,100,340,-2.5,[(290,326,82)],[(112,196,40,84),(214,262,44,76)],102),
 ("H",120,0,100,-2.5,[],[],102),
 ("H",120,100,192,-2.5,[],[],102),
 ("H",192,100,276,-2.5,[(150,186,80),(206,244,84)],[],102),
 ("H",192,276,340,-2.5,[(296,334,84)],[],102),
 ("H",240,0,144,-2.5,[],[],102),
 ("H",348,0,144,-2.5,[],[],102),
 ("H",348,144,192,-2.5,[(150,186,80)],[],102),
 ("H",417,62,144,-2.5,[],[],102),
 ("H",519,192,340,-2.5,[(222,310,84)],[],102),
 ("H",553,62,192,-2.5,[],[(92,168,30,90)],102),
 ("V",0,348,445,2.5,[],[],42),
 ("H",445,0,62,-2.5,[],[],42),
]

def walls():
    out = []
    for (o, c, a0, a1, e, doors, wins, h) in WALLS:
        s, L = a0 - e, a1 + e
        cuts = sorted([(a, b, 0, dz) for (a, b, dz) in doors] + list(wins))
        segs = []; u = s
        for (a, b, z0, z1) in cuts:
            if a > u: segs.append((u, a, 0, h))
            if z0 > 0: segs.append((a, b, 0, z0))
            if z1 < h: segs.append((a, b, z1, h))
            u = b
        if L > u: segs.append((u, L, 0, h))
        for (u0, u1, z0, z1) in segs:
            if o == "V": out.append(P(100, "b", (c - T / 2, u0, z0, c + T / 2, u1, z1)))
            else: out.append(P(100, "b", (u0, c - T / 2, z0, u1, c + T / 2, z1)))
    return out

def parse(line):
    mi, kind, ms, bb, extra = line.split("|")
    if ms[0] == "T":
        t = tuple(float(v) for v in ms[1:].split(",")); R = I3
    else:
        v = [float(x) for x in ms[1:].split(",")]
        cols = [v[0:3], v[3:6], v[6:9]]
        R = [[cols[j][i] for j in range(3)] for i in range(3)]
        t = tuple(v[9:12])
    box = tuple(float(x) for x in bb.split(","))
    p = P(int(mi), kind, box, R=R, t=t)
    if kind == "r":
        p["r"] = float(extra)
        if p["r"] < 0.2: p["kind"] = "b"
    elif kind == "c":
        p["prof"] = [tuple(float(a) for a in q.split(":")) for q in extra.split(";")]
    return p

def all_prims():
    prims = []
    for blob in (PART1, PART2):
        for line in blob.strip().splitlines():
            line = line.strip()
            if not line: continue
            if line == "FLUTE": prims += [bx(10, 336, 382 + k * 4, 0, 1.5, 3.6, 96) for k in range(30)]; continue
            if line == "CHAIRS": prims += chairs(); continue
            if line == "SKIRT": prims += skirting(); continue
            if line == "HSLATS": prims += [bx(10, 186.5, 440 + k * 4.3, 0, 2, 2.6, 80) for k in range(22)]; continue
            if line == "SHRUBS":
                prims += [P(36 if k % 2 else 16, "c", None, t=(200 + k * 16, 572.5, 20), prof=[(0, 4), (5, 7), (11, 6), (15, 1)]) for k in range(9)]
                continue
            prims.append(parse(line))
    return prims + walls()

# ------------------------------------------------------------------ geometry (faces as polygons, groups split for shading)
def box_faces(x0, y0, z0, x1, y1, z1):
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    q = [[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7],[0,3,2,1]]
    return [([v[i] for i in f], False, k) for k, f in enumerate(q)]

def rbox_faces(x0, y0, z0, x1, y1, z1, r, n=5):
    w, d = x1 - x0, y1 - y0
    r = max(0.05, min(r, w / 2 - 0.01, d / 2 - 0.01))
    cs = [(r, r), (w - r, r), (w - r, d - r), (r, d - r)]
    sa = [math.pi, 1.5 * math.pi, 0, 0.5 * math.pi]
    ring = []
    for ci in range(4):
        for j in range(n + 1):
            a = sa[ci] + (math.pi / 2) * j / n
            ring.append((x0 + cs[ci][0] + r * math.cos(a), y0 + cs[ci][1] + r * math.sin(a)))
    m = len(ring); out = []
    for i in range(m):
        a, b = ring[i], ring[(i + 1) % m]
        out.append(([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], True, "side"))
    out.append(([(p[0], p[1], z1) for p in ring], False, "top"))
    out.append(([(p[0], p[1], z0) for p in reversed(ring)], False, "bot"))
    return out

def cyl_faces(prof, n=36):
    ang = [2 * math.pi * i / n for i in range(n)]
    rings = [[(r * math.cos(a), r * math.sin(a), z) for a in ang] for (z, r) in prof]
    out = []
    for k in range(len(rings) - 1):
        A, B = rings[k], rings[k + 1]
        for j in range(n):
            j2 = (j + 1) % n
            out.append(([A[j], A[j2], B[j2], B[j]], True, "side"))
    out.append((list(reversed(rings[0])), False, "bot"))
    out.append((list(rings[-1]), False, "top"))
    return out

def xform(p, pt):
    R, t = p["R"], p["t"]
    return Vector(((R[0][0]*pt[0] + R[0][1]*pt[1] + R[0][2]*pt[2] + t[0]) * IN,
                   (R[1][0]*pt[0] + R[1][1]*pt[1] + R[1][2]*pt[2] + t[1]) * IN,
                   (R[2][0]*pt[0] + R[2][1]*pt[1] + R[2][2]*pt[2] + t[2]) * IN))

# ------------------------------------------------------------------ materials
def node_mat(name, color, alpha):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    base = (*color, 1.0)
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Roughness"].default_value = 0.6
    L = nt.links
    def tex_coord():
        tc = nt.nodes.new("ShaderNodeTexCoord"); return tc.outputs["Object"]
    def mix_color(fac_socket, c1, c2):
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
        L.new(fac_socket, mx.inputs["Factor"])
        mx.inputs[6].default_value = (*c1, 1); mx.inputs[7].default_value = (*c2, 1)
        return mx.outputs[2]
    def darker(c, f): return tuple(max(0, x * f) for x in c)
    def bump(height_socket, strength):
        b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = strength
        b.inputs["Distance"].default_value = 0.002
        L.new(height_socket, b.inputs["Height"]); L.new(b.outputs[0], bsdf.inputs["Normal"])
    n = name
    if any(k in n for k in ("Oak", "Walnut", "Teak", "Deck")) :
        # wood grain: stretched noise + wave
        co = tex_coord()
        mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 18.0, 1.0)
        L.new(co, mp.inputs[0])
        if "Floor" in n or "Deck" in n:
            mp.inputs["Scale"].default_value = (2.0, 30.0, 2.0)
        noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 6.0
        noise.inputs["Detail"].default_value = 8.0
        L.new(mp.outputs[0], noise.inputs[0])
        wave = nt.nodes.new("ShaderNodeTexWave"); wave.inputs["Scale"].default_value = 14.0
        wave.inputs["Distortion"].default_value = 2.5; wave.wave_type = "BANDS"; wave.bands_direction = "X"
        L.new(mp.outputs[0], wave.inputs[0])
        mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"
        L.new(noise.outputs[0], mm.inputs[0]); L.new(wave.outputs[1], mm.inputs[1])
        col = mix_color(mm.outputs[0], darker(color, 1.12), darker(color, 0.72))
        L.new(col, bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.42 if "Floor" in n else 0.5
        bump(mm.outputs[0], 0.08)
        if "Floor" in n:
            # plank seams
            br = nt.nodes.new("ShaderNodeTexBrick")
            br.inputs["Scale"].default_value = 1.0
            br.inputs["Mortar Size"].default_value = 0.004
            br.inputs["Brick Width"].default_value = 1.2; br.inputs["Row Height"].default_value = 0.19
            br.offset = 0.37
            L.new(co, br.inputs[0])
            bump(br.outputs["Fac"], 0.25)
    elif "Boucle" in n or "Rug" in n or "Fabric" in n or "Cushion" in n or "Bedding" in n or "Headboard" in n or "Curtain" in n or "Linen" in n or "Cane" in n or "Rattan" in n:
        co = tex_coord()
        vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260.0 if "Boucle" in n else 180.0
        L.new(co, vor.inputs[0])
        noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 40.0
        L.new(co, noise.inputs[0])
        col = mix_color(noise.outputs[0], darker(color, 1.06), darker(color, 0.88))
        L.new(col, bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.9
        bsdf.inputs["Sheen Weight"].default_value = 0.4
        bump(vor.outputs[0], 0.35 if ("Boucle" in n or "Rug" in n or "Rattan" in n or "Cane" in n) else 0.12)
        if "Curtain" in n or "Linen_Curtain" in n:
            bsdf.inputs["Transmission Weight"].default_value = 0.35
            wave = nt.nodes.new("ShaderNodeTexWave"); wave.inputs["Scale"].default_value = 18
            wave.bands_direction = "X"; L.new(co, wave.inputs[0]); bump(wave.outputs[1], 0.6)
    elif n == "Glass":
        bsdf.inputs["Base Color"].default_value = (0.95, 0.97, 0.98, 1)
        bsdf.inputs["Transmission Weight"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.0
        bsdf.inputs["IOR"].default_value = 1.45
    elif n == "Warm_Light":
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.72, 0.42, 1)
        bsdf.inputs["Emission Strength"].default_value = 8.0
    elif "Lamp_Shade" in n:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.78, 0.5, 1)
        bsdf.inputs["Emission Strength"].default_value = 0.8
        bsdf.inputs["Transmission Weight"].default_value = 0.5
    elif "Brass" in n:
        bsdf.inputs["Metallic"].default_value = 1.0; bsdf.inputs["Roughness"].default_value = 0.28
    elif n in ("Black_Frame", "Frame_Bronze", "Appliance_Steel"):
        bsdf.inputs["Metallic"].default_value = 0.8; bsdf.inputs["Roughness"].default_value = 0.35
    elif "Quartz" in n or "Porcelain" in n or "Ceramic" in n:
        bsdf.inputs["Roughness"].default_value = 0.12
        bsdf.inputs["Coat Weight"].default_value = 0.4
        if "Quartz" in n:
            co = tex_coord(); nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 60
            L.new(co, nz.inputs[0]); L.new(mix_color(nz.outputs[0], color, darker(color, 0.93)), bsdf.inputs["Base Color"])
    elif "Zellige" in n:
        co = tex_coord()
        br = nt.nodes.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 12.0
        br.inputs["Mortar Size"].default_value = 0.012; br.inputs["Brick Width"].default_value = 0.5
        br.inputs["Row Height"].default_value = 0.5; br.offset = 0.0
        br.inputs["Color1"].default_value = (*darker(color, 1.08), 1); br.inputs["Color2"].default_value = (*darker(color, 0.82), 1)
        br.inputs["Mortar"].default_value = (0.85, 0.8, 0.72, 1)
        L.new(co, br.inputs[0]); L.new(br.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.15; bsdf.inputs["Coat Weight"].default_value = 0.8
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 25; L.new(co, nz.inputs[0])
        bump(nz.outputs[0], 0.15)
    elif "Terrazzo" in n or "Travertine" in n:
        co = tex_coord()
        vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 70.0 if "Terrazzo" in n else 8.0
        L.new(co, vor.inputs[0])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (*darker(color, 0.75), 1)
        ramp.color_ramp.elements[1].position = 0.25; ramp.color_ramp.elements[1].color = (*color, 1)
        L.new(vor.outputs[0], ramp.inputs[0]); L.new(ramp.outputs[0], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.25
    elif "Wall" in n or "Ceiling" in n or "Limewash" in n:
        co = tex_coord(); nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 3.0 if "Limewash" in n else 30.0
        nz.inputs["Detail"].default_value = 6
        L.new(co, nz.inputs[0])
        f = 0.85 if "Limewash" in n else 0.97
        L.new(mix_color(nz.outputs[0], color, darker(color, f)), bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.85
    elif n in ("TV_Black",):
        bsdf.inputs["Roughness"].default_value = 0.08
    elif "Plant" in n or n == "Olive_Green":
        bsdf.inputs["Roughness"].default_value = 0.55
        bsdf.inputs["Subsurface Weight"].default_value = 0.2
        co = tex_coord(); vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 90
        L.new(co, vor.inputs[0]); bump(vor.outputs[0], 0.9)
        L.new(mix_color(vor.outputs[0], darker(color, 1.15), darker(color, 0.55)), bsdf.inputs["Base Color"])
    elif "Cabinet" in n:
        bsdf.inputs["Roughness"].default_value = 0.35
    return m

# ------------------------------------------------------------------ build
def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for mesh in list(bpy.data.meshes): bpy.data.meshes.remove(mesh)
    for l in list(bpy.data.lights): bpy.data.lights.remove(l)
    for c in list(bpy.data.cameras): bpy.data.cameras.remove(c)

def build():
    clear()
    mats = load_mats()
    prims = all_prims()
    groups = {}
    for p in prims:
        groups.setdefault(p["mat"], []).append(p)
    objs = {}
    for mid, plist in groups.items():
        name, color, alpha = mats[mid]
        bm = bmesh.new()
        for p in plist:
            if p["kind"] == "b": faces = box_faces(*p["box"])
            elif p["kind"] == "r": faces = rbox_faces(*p["box"], p["r"])
            else: faces = cyl_faces(p["prof"])
            cache = {}
            for (pts, smooth, grp) in faces:
                vs = []
                for pt in pts:
                    key = (round(pt[0], 4), round(pt[1], 4), round(pt[2], 4), grp if not smooth else "s")
                    v = cache.get(key)
                    if v is None:
                        v = bm.verts.new(xform(p, pt)); cache[key] = v
                    vs.append(v)
                try:
                    f = bm.faces.new(vs); f.smooth = smooth
                except ValueError:
                    pass
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        me.materials.append(node_mat(name, color, alpha))
        objs[name] = ob
    # ground outside so the view through windows is not void
    bpy.ops.mesh.primitive_plane_add(size=200, location=(170 * IN, 290 * IN, -0.6))
    g = bpy.context.active_object; g.name = "Outdoor_Ground"
    g.data.materials.append(node_mat("Outdoor_Ground", (0.32, 0.36, 0.26), 1))
    return objs

def lights():
    sc = bpy.context.scene
    world = sc.world or bpy.data.worlds.new("World"); sc.world = world
    world.use_nodes = True; nt = world.node_tree; nt.nodes.clear()
    sky = nt.nodes.new("ShaderNodeTexSky")
    for st in ("MULTIPLE_SCATTERING", "SINGLE_SCATTERING", "NISHITA", "HOSEK_WILKIE"):
        try:
            sky.sky_type = st; break
        except Exception:
            pass
    for attr, val in (("sun_elevation", math.radians(28)), ("sun_rotation", math.radians(160)),
                      ("air_density", 1.2), ("dust_density", 1.5), ("aerosol_density", 1.5)):
        try: setattr(sky, attr, val)
        except Exception: pass
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs[1].default_value = 0.35
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(sky.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])
    # sun: late afternoon, streaming in through the balcony doors (north, +Y) and the west windows
    sd = bpy.data.lights.new("Sun", "SUN"); sd.energy = 4.5; sd.angle = math.radians(1.5)
    sd.color = (1.0, 0.9, 0.78)
    so = bpy.data.objects.new("Sun", sd); sc.collection.objects.link(so)
    direction = Vector((0.55, -0.62, -0.45)).normalized()   # light travels toward -Y, +X, downward
    so.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    def area(name, x, y, z, size, power, color=(1.0, 0.9, 0.78)):
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = power * 0.45; ld.size = size * IN; ld.color = color
        lo = bpy.data.objects.new(name, ld); lo.location = (x * IN, y * IN, z * IN)
        sc.collection.objects.link(lo)
    def point(name, x, y, z, power, radius=2.0, color=(1.0, 0.8, 0.6)):
        ld = bpy.data.lights.new(name, "POINT"); ld.energy = power; ld.shadow_soft_size = radius * IN; ld.color = color
        lo = bpy.data.objects.new(name, ld); lo.location = (x * IN, y * IN, z * IN)
        sc.collection.objects.link(lo)
    # soft ceiling fill per room (warm 3000K)
    for (n, x, y, s, pw) in [("L_Living", 265, 440, 60, 140), ("L_Dining", 250, 275, 50, 90), ("L_Kitchen", 190, 100, 60, 130),
                              ("L_Master", 127, 485, 50, 90), ("L_Bed2", 70, 294, 40, 60), ("L_Bed3", 50, 180, 40, 60),
                              ("L_Bath", 146, 156, 24, 30), ("L_MBath", 100, 382, 24, 30), ("L_Hall", 170, 300, 24, 25),
                              ("L_Foyer", 308, 90, 24, 30)]:
        area(n, x, y, 100.5, s, pw)
    # practical lights
    point("P_Pendant_1", 228, 274, 62, 30); point("P_Pendant_2", 260, 274, 62, 30)
    point("P_Island_1", 166, 72, 66, 18); point("P_Island_2", 190, 72, 66, 18)
    point("P_FloorLamp", 206, 500, 58, 25); point("P_Bedside_1", 177, 442, 33, 12); point("P_Bedside_2", 177, 532, 33, 12)
    point("P_Master_Ceiling", 140, 487, 92, 20)

def camera(name, eye, target, hfov=78, lens_shift_y=0.0):
    cd = bpy.data.cameras.new(name); cd.sensor_fit = "HORIZONTAL"; cd.angle = math.radians(hfov)
    cd.shift_y = lens_shift_y; cd.clip_start = 0.05
    co = bpy.data.objects.new(name, cd); bpy.context.scene.collection.objects.link(co)
    e = Vector(eye) * IN; t = Vector(target) * IN
    co.location = e
    co.rotation_euler = (t - e).to_track_quat("-Z", "Y").to_euler()
    return co

VIEWS = [
    # name, eye(in), target(in), hfov, shift, hide ceiling?
    ("01_Living_from_Dining", (302, 203, 56), (240, 470, 44), 76, 0.0, False),
    ("02_Dining_from_Living", (300, 470, 58), (238, 262, 40), 80, 0.0, False),
    ("03_Kitchen", (232, 178, 62), (170, 30, 40), 84, 0.0, False),
    ("04_Master_Bedroom", (70, 505, 58), (186, 478, 44), 88, 0.0, False),
    ("05_Overview_Dollhouse", (170, -330, 640), (170, 290, 0), 52, 0.0, True),
]

def render_all():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "NONE"
        sc.cycles.device = "CPU"
    except Exception as ex:
        print("GPU setup failed:", ex)
    sc.cycles.samples = 24 if QUICK else 96
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.render.threads_mode = "AUTO"
    sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 5; sc.cycles.glossy_bounces = 4
    sc.cycles.transmission_bounces = 8; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
    sc.render.resolution_x = 960 if QUICK else 1600
    sc.render.resolution_y = 540 if QUICK else 900
    sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 92
    for vt in ("AgX", "Filmic"):
        try: sc.view_settings.view_transform = vt; break
        except Exception: pass
    for lk in ("AgX - Punchy", "Punchy", "AgX - Medium High Contrast", "Medium High Contrast"):
        try: sc.view_settings.look = lk; break
        except Exception: pass
    sc.view_settings.exposure = 0.6
    which = []
    queue = [v for v in VIEWS if not which or v[0] in which]
    for v in queue:
        camera(v[0], v[1], v[2], v[3], v[4])
    state = {"queue": queue, "cur": None}

    def log(msg):
        with open(os.path.join(OUT, "progress.txt"), "a") as f: f.write(msg + "\n")

    def start_next():
        if not state["queue"]:
            log("ALL DONE")
            with open(os.path.join(OUT, "DONE.txt"), "w") as f: f.write("done")
            return None
        name, eye, target, hfov, shift, hide_ceiling = state["queue"].pop(0)
        state["cur"] = name
        sc.camera = bpy.data.objects[name]
        ceiling = bpy.data.objects.get("Ceiling_Warm_White")
        if ceiling: ceiling.hide_render = hide_ceiling
        sc.view_settings.exposure = -0.3 if hide_ceiling else -0.15
        sc.render.filepath = os.path.join(OUT, name + ".jpg")
        log("rendering " + name)
        win = bpy.context.window_manager.windows[0]
        with bpy.context.temp_override(window=win):
            bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
        return None

    def on_done(scene, *args):
        log("saved " + str(state["cur"]))
        bpy.app.timers.register(start_next, first_interval=1.0)

    for h in list(bpy.app.handlers.render_complete):
        if getattr(h, "__name__", "") == "on_done": bpy.app.handlers.render_complete.remove(h)
    bpy.app.handlers.render_complete.append(on_done)
    bpy.app.timers.register(start_next, first_interval=0.5)

build()
lights()
render_all()
