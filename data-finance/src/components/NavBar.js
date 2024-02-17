import React from 'react'
import styles from './NavBar.module.css'
import Carousel from './Carousel'

function navbar(){
    return(
        <>
        <nav className={`navbar sticky-top navbar-light ${styles['custom-navbar']}`}>
            <div className="container-fluid justify-content-center">               
                
                <ul className={`${styles['menuItem']} list-inline`}>
                
                    <li id="info" className=" list-inline-item nav-item dropdown">
                        
                        <a className="dropdown text-decoration-none text-white" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#" >
                          INFO
                        </a>
                        <div id="mostrar" className={`dropdown-menu ${styles['mostrar']}`} aria-labelledby="navbarDropdownMenuLink">
                        <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                          </div>
                    </li>

                    <li id="info" className=" list-inline-item nav-item dropdown">
                        
                        <a className="dropdown text-decoration-none text-white" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#" >
                          INFO
                        </a>
                        <div id="mostrar" className={`dropdown-menu ${styles['mostrar']}`} aria-labelledby="navbarDropdownMenuLink">
                        <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                          </div>
                    </li>
                    
                    <li id="info" className="list-inline-item nav-item dropdown">
                        <a className="dropdown text-decoration-none text-white" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#" >
                          INFO
                        </a>
                        <div id="mostrar" className={`dropdown-menu ${styles['mostrar']}`} aria-labelledby="navbarDropdownMenuLink">
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                          </div>
                    </li> 

                    <li id="info" className="list-inline-item nav-item dropdown">
                        <a className="dropdown text-decoration-none text-white" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#" >
                            INFO
                        </a>
                        <div id="mostrar" className={`dropdown-menu ${styles['mostrar']}`} aria-labelledby="navbarDropdownMenuLink">
                        <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                            <a className="dropdown-item" href="#">#######</a>
                          </div>
                    </li> 

                </ul>
            </div> 
                  
        </nav>
        <Carousel/>
        
                
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.6/dist/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.2.1/dist/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
    
        </>
    )
}

export default navbar