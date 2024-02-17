import React from 'react'
import styles from "./Corpo.module.css"

import Table from './Table'


function corpo(){
    return(
      <>
      <div className={styles.containerMain}>
        <div className={`container-fluid ${styles.container}`}>
  <div className="row">
    <nav className={`col-2 d-inline-block ${styles.sidebar}`}>
      <div className="sidebar-sticky ">
        <ul className="nav flex-column">
          <li className="nav-item">
            <a className="nav-link active" href="#">
            <h6 className="sidebarHeading d-flex justify-content-between align-items-center mb-1 text-muted">
          <span className={styles.sidebarHeading}>dados</span>
          <a className="d-flex align-items-center text-muted" href="#">
            <span data-feather="plus-circle"></span>
          </a>
        </h6>
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="file"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="shopping-cart"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="users"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="bar-chart-2"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="layers"></span>
              info
            </a>
          </li>
        </ul>

        <ul className="nav flex-column">
          <li className="nav-item">
            <a className="nav-link active" href="#">
            <h6 className="sidebarHeading d-flex justify-content-between align-items-center mb-1 text-muted">
          <span className={styles.sidebarHeading}>dados</span>
          <a className="d-flex align-items-center text-muted" href="#">
            <span data-feather="plus-circle"></span>
          </a>
        </h6>
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="file"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="shopping-cart"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="users"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="bar-chart-2"></span>
              info
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="layers"></span>
              info
            </a>
          </li>
          
        </ul>
      </div>
      </nav>

      <div className={`container-fluid col-10 ${styles.dashboardItem}`}>
        <div className='row'>
          

        <div className={`col-8 ${styles.dashboard}`}><h3>Dashboard</h3></div>

        <div className='seach-buttons col-4'>
        <button type="button" class="btn btn-outline-primary import">Importar</button>
        <button type="button" class="btn btn-outline-secondary export">Exportar</button>
        <button type="button" class="btn btn-outline-success month">Mes</button> 
        </div>

        </div>   
        <hr></hr>
        <Table/>
      </div>
      </div>
      </div>
      
       

      </div>
      </>
    )
}

export default corpo