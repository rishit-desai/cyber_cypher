import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react';

function App()
{

	const [open, setOpen] = useState(0);
	const [high, setHigh] = useState(0);
	const [low, setLow] = useState(0);
	const [close, setClose] = useState(0);
	const [volume, setVolume] = useState(0);
	const [adjClose, setAdjClose] = useState(0);
	const [date, setDate] = useState(0);
	const [headline, setHeadline] = useState(0);
	const [isPrediction, setIsPrediction] = useState(false);
	const [prediction, setPrediction] = useState();

	function predict()
	{
		fetch(`/predict/${open}/${high}/${low}/${close}/${volume}/${adjClose}/${date}/${headline}`
		).then(res =>
		{
			res.json().then(data =>
			{
				setPrediction(data.prediction);
				setIsPrediction(true);
			})
		});
	}

	return (
		<div className="App">
			<header className="App-header">
				<div className="container">
					<h1>Stock Price prediction</h1>
					{isPrediction && <div className="row">
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Avg Price:</span> {prediction[0][0]}</div>
						</div>	
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Closing Price:</span> {prediction[0][1]}</div>
						</div>	
					</div>}
					<div className="row">
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Open:</span> <input onChange={(e) => setOpen(e.target.value)} value={open || ''} type="text" /></div>
						</div>
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>High:</span> <input onChange={(e) => setHigh(e.target.value)} value={high || ''} type="text" /></div>
						</div>
					</div>
					<div className="row">
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Low:</span> <input onChange={(e) => setLow(e.target.value)} value={low || ''} type="text" /></div>
						</div>
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Close:</span> <input onChange={(e) => setClose(e.target.value)} value={close || ''} type="text" /></div>
						</div>
					</div>
					<div className="row">
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Volume:</span> <input onChange={(e) => setVolume(e.target.value)} value={volume || ''} type="text" /></div>
						</div>
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Adj Close:</span> <input onChange={(e) => setAdjClose(e.target.value)} value={adjClose || ''} type="text" /></div>
						</div>
					</div>
					<div className="row">
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Date:</span> <input onChange={(e) => setDate(e.target.value)} value={date || ''} type="text" /></div>
						</div>
						<div className="col-md-6">
							<div class="wrapper"><span className='text-span'>Headline:</span> <input onChange={(e) => setHeadline(e.target.value)} value={headline || ''} type="text" /></div>
						</div>
					</div>
					<button onClick={predict}>Predict</button>
				</div>
			</header>
		</div>
	);
}

export default App;
