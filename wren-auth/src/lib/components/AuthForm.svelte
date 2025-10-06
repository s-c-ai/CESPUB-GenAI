<script lang="ts">
  import Icon from "@iconify/svelte";

  import logoImage from "$assets/logo-with-text.svg";
  import { LoginButton } from "$components";
</script>

<div
  class="px-15 py-31 auth-border flex flex-col justify-center w-full h-full items-center md:items-start"
>
  <img src={logoImage} alt="" class="mb-10 w-100 h-20" />
  <h1 class="text-center md:text-start text-dark-blue font-bold text-5xl mb-6">
    Log in to your account
  </h1>
  <h2 class="text-dark-blue font-medium text-2xl mb-10">Welcome back!</h2>
  <form
    method="post"
    class="auth-form flex flex-col w-full h-full items-center"
  >
    <LoginButton type="submit">
      <Icon icon="logos:google-icon" width="24" height="24" />
      <span class="text-sm text-dark-blue">Login with Google account</span>
    </LoginButton>
  </form>
  <p class="text-dark-blue text-xs mt-6">
    Problems to log in your account? <a
      class="text-primary font-bold text-xs cursor-pointer"
      href="mailto:claudinho@s-c.ai">Send us an email</a
    >
  </p>
</div>

<style>
  .auth-border {
    border: double 1px transparent;
    border-radius: 12px;
    border-image: linear-gradient(
        21deg,
        rgba(253, 253, 253, 1) 60%,
        rgba(253, 200, 49, 1) 100%
      )
      1;
    background-origin: border-box;
    background-clip: content-box, border-box;
  }
</style>
