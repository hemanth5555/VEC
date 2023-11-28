import './HomePage.css'
import ImageUploader from '../ImageUploader/ImageUploader'
import NavBar from '../NavBar/NavBar'
import SideBar from '../SideBar/SideBar'
import React, { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom';

function HomePage() {
  const [showComponent, setShowComponent] = useState(null);
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;

  const location = useLocation();
  const navigate = useNavigate();
  const session_token = localStorage.getItem('session_token');
  console.log('session_token  ' + session_token)
  const username = localStorage.getItem('username');
  useEffect(() => {
  if(session_token)
  {
    console.log("Use effect")
    fetch(baseuri + `/is_authenticated`, {
      headers: {
        "session-token": session_token
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.response)
        data = data.response
        if(!data)
        {
          console.log('No user session')
          localStorage.removeItem('session_token');
          localStorage.removeItem('username');
          navigate('/loginpage');
        }

      })
      .catch(error => {
          console.log('No user session', error)
          localStorage.removeItem('session_token');
          localStorage.removeItem('username');
          navigate('/loginpage');
      });
  }
  else{
        console.log("No session variable")
        localStorage.removeItem('session_token');
        localStorage.removeItem('username');
        navigate('/loginpage');
  }
}, []);

  const handleComponentToggle = (component) => {
    setShowComponent(component);
    console.log('Toggling component:', component);
  }

  const handleHomeClick = () => {
    console.log('Home clicked');
    setShowComponent(null);
  }

  const handleSettingsClick = () => {
    setShowComponent(null);
  }

  let componentToRender;
  if (showComponent === 'upload') {
    componentToRender = <ImageUploader session_token={session_token} />;
  } 

  return (
    <div className="content">
      <NavBar username={username} session_token={session_token}/>

      <div className="sidebar-container">
        <SideBar onUploadClick={() => handleComponentToggle('upload')} 
        onSettingsClick={() => handleSettingsClick()}
        onHomeClick={() => handleHomeClick()}/>
        {componentToRender}
      </div>
    </div>
  )
}

export default HomePage;

