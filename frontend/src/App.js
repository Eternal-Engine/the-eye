//App component serves as container to our application. exported as child to ./index.js

import Header from "./components/Header"  //import header component from components
import headlines from './data/news'  //model data

function App(){
 
    return (
        <>   
        <Header />
        <div className="container">
            
        </div>
        </>
        
    )
}



export default App