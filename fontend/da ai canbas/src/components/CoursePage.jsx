




import { useParams } from "react-router";

export function CoursePage() {
  const { id } = useParams();
  return <main className="dash-main"><h1 className="dash-title">Course {id}</h1></main>;
}