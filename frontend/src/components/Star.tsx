type StarRating = {
  id: string;
  size: number;     // width & height in px
  color: string;    // fill color
  fillPercent: number;
};

export default function Star({
  id,
  size,
  color,
  fillPercent
}: StarRating) {
    const points = getStarPoints(10)
      // Compute min/max bounds
    const xs = points.map(p => p.x);
    const ys = points.map(p => p.y);

    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    const viewWidth = maxX - minX;
    const viewHeight = maxY - minY;

    // Render as size(px) * size(px) = width * height
    // viewBox = "minX, minY, width, height." Scaled to width * height.
    return (
        <svg 
          width={size} 
          height={size} 
          viewBox={`${minX} ${minY} ${viewWidth} ${viewHeight}`}
        >
          <defs>
            <linearGradient id={`partialFill-${id}`} x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset={`${fillPercent}%`} stopColor={color} />
              <stop offset={`${fillPercent}%`} stopColor="lightgray" />
            </linearGradient>
          </defs>
            <polygon
                points={points.map(p => `${p.x},${p.y}`).join(" ")}
                fill={`url(#partialFill-${id})`}
                stroke="black"
                strokeWidth={0.1}
            />
        </svg>
    );
}

function getOuterPoints(edgeLength: number) {
  return getPentagonPoints(edgeLength, -Math.PI / 2, false);
}

function getInnerPoints(edgeLength: number) {
  const step = (2 * Math.PI) / 5;
  return getPentagonPoints(edgeLength, -Math.PI / 2 + 3 * step, true);
}

function getPentagonPoints(
  edgeLength: number,
  startAngle: number,
  flip: boolean = false
) {
  const points = [];
  const step = (2 * Math.PI) / 5; // 72 degrees
  const R = edgeLength / (2 * Math.sin((72 * Math.PI) / 180));
  
  for (let k = 0; k < 5; k++) {
    const angle = startAngle + k * step;
    let x = R * Math.cos(angle);
    let y = R * Math.sin(angle);
    if (flip) {
      x = -x;
      y = -y;
    }
    points.push({x, y})
  }
  return points
}

function getStarPoints(edgeLength: number) {
  const points = [];
  let outerIdx = 0;
  let innerIdx = 0;

  const innerEdgeLength = edgeLength / 2;
  const outerPoints = getOuterPoints(edgeLength);
  const innerPoints = getInnerPoints(innerEdgeLength);

  for (let i = 0; i < 10; i++) {
    if (i % 2 === 0) {
      points.push(outerPoints[outerIdx]);
      outerIdx += 1;
    } else {
      points.push(innerPoints[innerIdx]);
      innerIdx += 1;
    }
  }

  return points;
}
