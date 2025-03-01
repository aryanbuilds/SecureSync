function doFilter(req, res, next) {
  // Log the URL of the incoming request
  console.debug("doFilter url: " + req.originalUrl);

  // Authenticate the user; assume authenticateUser returns a boolean
  const isAuthenticated = authenticateUser(req);

  // If user is not authenticated
  if (!isAuthenticated) {
    // Try to get the SAMLResponse parameter from query or body
    const samlLogoutRequest = req.query.SAMLResponse || req.body?.SAMLResponse;
    console.info("samlResponse --> " + samlLogoutRequest);

    if (samlLogoutRequest) {
      // If there's a SAMLResponse, handle it and exit this middleware
      return handleSAMLResponse(req, res, next, samlLogoutRequest);
    } else {
      // If no SAMLResponse, check if this is a Starship request
      if (isStarshipRequest(req)) {
        // Ensure a session exists; Express-session middleware should provide req.session
        let session = req.session;
        let userBean = session && session.USER_IN_SESSION;
        
        // If there is no userBean in session, create one
        if (!userBean) {
          try {
            userBean = {
              credentialId: "",
              adminPasswordReset: true,
              productId: "cloupia_service_portal",
              profileId: 0,
              // Get headers similar to the Java version
              restKey: req.get("X-Starship-Request-Key"),
              starshipUserId: req.get("X-Starship-UserName-Key"),
              loginName: "admin",
              starshipSessionId: req.get("X-Starship-UserSession-Key")
            };
            
            // Retrieve requested URI or role from header
            const requestedUri = req.get("X-Starship-UserRoles-Key");
            userBean.accessLevel = requestedUri;
            
            // If the requested role is "admin", update access level and evaluate allowed operations
            if (requestedUri && requestedUri.toLowerCase() === "admin") {
              const authmgr = AuthenticationManager.getInstance();
              userBean.accessLevel = "Admin";
              authmgr.evaluateAllowedOperations(userBean);
            }
            
            // Save userBean and default URL in the session
            req.session.USER_IN_SESSION = userBean;
            req.session.DEFAULT_URL = STARSHIP_DEFAULT_URL;
            console.info("userBean:" + userBean.accessLevel);
          } catch (error) {
            console.info("username/password wrong for rest api access - " + error.message);
          }
          console.info("userBean: " + userBean.accessLevel);
        }
        // Continue processing after setting up the session
        return next();
      }
    }
  }
  
  // If user is authenticated, or none of the special branches applied, simply continue
  return next();
}

/*
 * Helper functions (stubs) for demonstration:
 */
function authenticateUser(req) {
  // Your authentication logic goes here
  // Return true if authenticated, false otherwise
  return false;
}

function handleSAMLResponse(req, res, next, samlLogoutRequest) {
  // Your SAML response handling logic goes here.
  // When done, call next() or end the response.
  console.info("Handling SAML response: " + samlLogoutRequest);
  // For example purposes, simply continue:
  return next();
}

function isStarshipRequest(req) {
  // Determine if this request qualifies as a Starship request.
  // For example, check for a specific header:
  return req.get("X-Starship-Request-Key") !== undefined;
}

// Stub for AuthenticationManager singleton
const AuthenticationManager = {
  getInstance: function() {
    return {
      evaluateAllowedOperations: function(userBean) {
        // Evaluation logic for allowed operations goes here
      }
    };
  }
};

// Define your default URL constant
const STARSHIP_DEFAULT_URL = "/defaultStarshipUrl";

// Export the middleware function for use in an Express app
module.exports = doFilter;
