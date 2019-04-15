convert -background #00000080 -pointsize 100 -fill white label:"A" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - 15309700.jpg"[50%%]" seg1.png

convert -background #00000080 -pointsize 100 -fill white label:"B" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - 15309700.class.png"[50%%]" seg2.png

convert -background #00000080 -pointsize 100 -fill white label:"C" -gravity southeast -splice 20x0  -gravity northwest -splice 20x0 miff:- | composite -gravity northeast -geometry +10+10 - 15309700.object.png"[50%%]" seg3.png

montage seg1.png seg2.png seg3.png -tile 3x1 -geometry +0+0 seg.png