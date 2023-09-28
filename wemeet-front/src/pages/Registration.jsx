import React from "react"

import { Link } from "react-router-dom"

import RegistrationForm from "../components/authentication/RegistrationForm"

function Registration() {
	return (
		<div className="container">
			<div className="row">
				<div className="col-md-6 d-flex align-items-center">
					<div className="content text-center px-4">
						<h1 className="text-primary">위밋</h1>
						<p className="content">
							위밋 앱에 오신걸 환영합니다.<br />
							이미 계정이 있다면 {" "}
							<Link to="/login/">로그인 하기</Link>
						</p>
					</div>
				</div>
				<div className="col-md-6 p-5">
					<RegistrationForm />
				</div>
			</div>
		</div>
	)
}

export default Registration