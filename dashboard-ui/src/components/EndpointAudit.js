import React, { useEffect, useState } from 'react'
import '../App.css';

export default function EndpointAudit(props) {
    const [isLoaded, setIsLoaded] = useState(false);
    const [log, setLog] = useState(null);
    const [error, setError] = useState(null)
	//const rand_val = Math.floor(Math.random() * 100); // Get a random event from the event store
    const [index, setIndex] = useState(null);  //this
    // setIndex(rand_val);

    const getAudit = () => {
        const rand_val = Math.floor(Math.random() * 100);
        fetch(`http://lab6-servicebased.eastus.cloudapp.azure.com/audit_log/${props.endpoint}?index=${rand_val}`)
        // fetch(`http://lab6-servicebased.eastus.cloudapp.azure.com/${props.endpoint}?index=2`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Audit Results for " + props.endpoint)
                setLog(result);
                setIsLoaded(true);
                setIndex(rand_val); //This
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
	useEffect(() => {
		const interval = setInterval(() => getAudit(), 4000); // Update every 4 seconds
		return() => clearInterval(interval);
    }, [getAudit]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        
        return ( //Added index instead of random val
            <div>
                <h3>{props.endpoint}-{index}</h3> 
                {JSON.stringify(log)}
            </div>
        )
    }
}
