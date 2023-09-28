import React from "react"
import { Link } from "react-router-dom"
import LoginForm from "../components/authentication/LoginForm"

function Login() {
	return (
		<div className="container">
			<div className="row">
				<div className="col-md-6 d-flex align-items-center">
					<div className="content text-center px-4">
						<h1 className="text-primary">위밋!</h1>
						<p className="content">
							위밋에 로그인해주세요! <br />
							계정이 없다면 {" "}
							<Link to="/register/">가입하기</Link>.
						</p>
					</div>
				</div>
				<div className="col-md-6 p-5">
					<LoginForm />
				</div>
			</div>
		</div>
	)
}

export default Login