import Link from "next/link";
import Logo from "./Logo";
import ButtonSecondary from "./ButtonSecondary";
import { ArrowTopRightOnSquareIcon, UserIcon } from "@heroicons/react/20/solid";
import ButtonPrimary from "./ButtonPrimary";

const SmallNav = () => (
  <nav className="flex justify-between py-2">
    <Link href={"/"} className="group inline-flex items-center gap-2 p-2">
      <Logo></Logo>
      <span className="hidden font-bold group-hover:underline sm:inline">
        PaDDeL
      </span>
    </Link>
    <div className="flex items-center gap-2">
      <a href={`${process.env.NEXT_PUBLIC_API_LOCATION}/docs`} target="_blank">
        <ButtonSecondary>
          API Docs
          <ArrowTopRightOnSquareIcon
            className="-ml-0.5 h-5 w-5"
            aria-hidden="true"
          />
        </ButtonSecondary>
      </a>
      <Link href={"/admin"}>
        <ButtonPrimary>
          Admin
          <UserIcon className="-ml-0.5 h-5 w-5" aria-hidden="true"></UserIcon>
        </ButtonPrimary>
      </Link>
    </div>
  </nav>
);

export default SmallNav;
