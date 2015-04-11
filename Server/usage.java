/*1. Register a user with the system

	You need to make a request to the URL: http://sever_ip:27015/register?<params>
	where params are parameters for the registration
	
	- fb_id - The user's facebook id
	- real_name - The user's real name
	
	Example: http://127.0.0.1:27015/register?fb_id='123456'&real_name='Ivan Dortulov'
	
	The server will return a response containing a code indicating whether the
	operation was successful or not and an error message if an error has occured.
	
	Example code:
*/
		String URL = "http://127.0.0.1:27015/register?fb_id='123456'&real_name='Ivan Dortulov'";
		HttpClient httpclient = new DefaultHttpClient();
		HttpResponse response = httpclient.execute(new HttpGet(URL));
		StatusLine statusLine = response.getStatusLine();
		if(statusLine.getStatusCode() == HttpStatus.SC_OK){
			ByteArrayOutputStream out = new ByteArrayOutputStream();
			response.getEntity().writeTo(out);
			String responseString = out.toString();
			out.close();
    		
			switch(Integer.parseInt(responseString[0])) {
				case 1: {
					// User was registered without errors.
					break;
				} case 2: {
					// The user already registered.
					break;
				} case 3: {
					// Error has occured
					Log.e("Client", "Error occured: " + responseString);
					break;
				}
			}
		} else{
			//Closes the connection.
			response.getEntity().getContent().close();
			throw new IOException(statusLine.getReasonPhrase());
		}
    	
/* 2. Get a random picture
	
	You need to make a request to the URL: http://server_ip:27015/get_pic?<params>
	where params are parameters for the picture selection
	
	- fb_id - The user's facebook id
	- category - The pictures category
	
	Exaple: http://127.0.0.1:27015/get_pic?fb_id='123456'&category='space'
	
	The server will return an image.
	
	Example code:
*/

	String URL = "http://127.0.0.1:27015/get_pic?fb_id='123456'&category='space'"HttpClient httpclient = new DefaultHttpClient();
	HttpResponse response = httpclient.execute(new HttpGet(URL));
	StatusLine statusLine = response.getStatusLine();
	if(statusLine.getStatusCode() == HttpStatus.SC_OK){
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		response.getEntity().writeTo(out);
		String responseString = out.toString();
		out.close();
	
		String[] lines = responseString.readlines();
		String imageId = Integer.parseInt(lines[0]);
		String imageURL = lines[1];
	
		Picasso.with(context).load(imageURL).into(imageView);
	} else{
		//Closes the connection.
		response.getEntity().getContent().close();
		throw new IOException(statusLine.getReasonPhrase());
	}
	
/* 3. Give a space

	You need to make a request to the UR: http://server_ip:27015/space?<params>
	where params are parameters for the picture selection
	
	- fb_id - User's facebook id
	- pic_id - Pictures id
	- space - Space or not (1 or 0)
	
	Example: http://127.0.0.1:27015/space?fb_id='123456'&pic_id='15'&space='1'
*/
