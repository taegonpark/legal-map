import "../index.css"
import Star from "./Star"

export type AttorneyCardProps = {
  name: string;
  rating: number;
  address: string;
  phone: string;
  practices?: string[];
  languages?: string[];
};

export default function AttorneyCard({
  name, 
  rating, 
  address, 
  phone, 
  practices, 
  languages
}: AttorneyCardProps) {
  return (
    <div className="attorney-card-container">
        <div className="attorney-label-small"> {name}    </div>
        <div className="attorney-label-small flex gap-0.5">
          {rating}
          <div className="flex items-center gap-0.5">
            {[...Array(5)].map((_, i) => {
              const starNumber = i + 1;
              let fill = 0;

              if (rating >= starNumber) { fill = 100; } 
              else { fill = 100 * (rating - i); }

              // need an id to differentiate each linear gradient.
              return (
                <Star 
                  id = {`star-${i}`} 
                  key = {i}
                  size={10} 
                  color="#fcd34d" 
                  fillPercent = {fill}
                />
              );
            })}
          </div>
        </div>
        <div className="attorney-label-small"> {address} </div>
        <div className="attorney-label-small"> {phone}   </div>

        <div className="attorney-label-large"> {"Practice Areas: "   + practices?.join(", ")}   </div>
        <div className="attorney-label-large"> {"Languages (Self): " + languages?.join(", ")}   </div>
    </div>
  );
}