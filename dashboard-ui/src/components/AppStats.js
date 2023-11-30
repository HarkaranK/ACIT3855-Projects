import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://lab6-servicebased.eastus.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						{/* <tr>
							<th>Blood Pressure</th>
							<th>Heart Rate</th>
						</tr>
						<tr>
							<td># BP: {stats['num_bp_readings']}</td>
							<td># HR: {stats['num_hr_readings']}</td>
						</tr> */}
						<tr>
							<th>Weight</th>
							<th>Macros</th>
						</tr>
						<tr>
							<td># Num W: {stats['num_weight_readings']}</td>
							<td># Num M: {stats['num_macro_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Weight Reading: {stats['max_weight_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Protein Reading: {stats['max_protein_readings']}</td>
						</tr>
						{/* <tr>
							<td colspan="2">Max HR: {stats['max_bp_sys_reading']}</td>
						</tr> */}
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
