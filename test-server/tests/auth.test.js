import * as chai from "chai";
import "dotenv/config";
import { default as chaiHttp, request } from "chai-http";

chai.use(chaiHttp);
const { expect } = chai;

const BASE_URL = process.env.FASTAPI_URL || 'http://localhost:8000';

describe("Auth API", () => {
  let authToken = "";

  describe("POST /api/v1/users/register", () => {
    it("should successfully register a new user", () => {
      return request
        .execute(BASE_URL)
        .post("/api/v1/users/register")
        .send({
          username: "test_user2",
          email: "test2@example.com",
          password: "secure123",
        })
        .then((res) => {
          expect(res).to.have.status(200);
          expect(res.body).to.have.property("username");
          expect(res.body).to.have.property("email");
          expect(res.body).to.have.property("id");
          expect(res.body.username).to.be.a("string");
          expect(res.body.email).to.be.a("string");
          expect(res.body.id).to.be.a("string");
        });
    });
  });

  describe("POST /api/v1/auth/login", () => {
    it("should successfully login with valid credentials", () => {
      return request
        .execute(BASE_URL)
        .post("/api/v1/auth/login")
        .send({
          email: "test2@example.com",
          password: "secure123",
        })
        .then((res) => {
          expect(res).to.have.status(200);
          expect(res.body).to.have.property("access_token");
          expect(res.body).to.have.property("token_type");
          expect(res.body.access_token).to.be.a("string");
          expect(res.body.token_type).to.equal("bearer");

          // Store the token for authenticated requests
          authToken = res.body.access_token;
        });
    });
  });

  describe("GET /api/v1/users/me", () => {
    it("should fail to access /me route without authentication", () => {
      return request
        .execute(BASE_URL)
        .get("/api/v1/users/me")
        .then((res) => {
          expect(res).to.have.status(401);
        })
        .catch((err) => {
          expect(err).to.have.status(401);
        });
    });
  });
});
