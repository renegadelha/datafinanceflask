import styles from "./Home.module.css"

import NavBar from "../components/NavBar"
import Carousel from "../components/Carousel"

function home(){
    return(
        <div className={styles.home}>
            <NavBar/>
        </div>
        
    )
}

export default home