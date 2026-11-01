import './Error.css';

export function Error(){
    return(
        <>
            <link rel="icon" type="image/svg+xml" href="../public/error.jpg" />
            <title>Error: 404</title>
            <div className="Error">
                Error: 404. This page does not exist.
            </div>
        </>
        
    );
}