// src/App.tsx
import AttorneyCard, {type AttorneyCardProps} from "./components/AttorneyCard";

const attorney: AttorneyCardProps = {
  name: "John Smith",
  rating: 4.4,
  address: "123 Main St",
  phone: "201-264-5254",
  practices: ["Personal Injury", "Public Injury"],
  languages: ["English", "Spanish", "French"]
};

export function App() {
  return (
    <div className="p-10">
        <AttorneyCard {...attorney} />
    </div>
  );
}

export default App;
